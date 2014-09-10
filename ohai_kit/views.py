try:
    from urllib.parse import urlparse
except ImportError:     # Python 2
    from urlparse import urlparse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, resolve_url
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login, login as __login
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django.contrib.staticfiles import finders

from ohai_kit.models import Project, ProjectSet, JobInstance, \
    WorkStep, WorkReceipt


def get_active_jobs(user, project=None):
    """
    Returns a list of active jobs for the current user, and optionally
    for a given project.  If the project is specified, then the return
    will be either a job or False.  If the project is not specified,
    the return will be a list.
    """
    querie = {
        "user" : user,
        "completion_time" : None,
        }
    if project is not None:
        querie["project"] = project
    found = JobInstance.objects.filter(**querie)
    if project is not None:
        assert len(found) <= 1
        if found:
            return found[0]
        else:
            return False
    return found


def trigger_login_redirect(request, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Code pulled from the auth module, because its nested, preventing reuse.
    """
    path = request.build_absolute_uri()
    # urlparse chokes on lazy objects in Python 3, force to str
    resolved_login_url = force_str(
        resolve_url(login_url or settings.LOGIN_URL))
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
        (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()
    return redirect_to_login(
        path, resolved_login_url, redirect_field_name)


def guest_only(view_function, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Replacement for @login_required decorator, so that only guests may
    access the wrapped view.  In this event, the user is probably
    "lost" so instead of redirecting to the login page, just redirect
    to "/".\
    """
    def wrapped_view(request, *args, **kwargs):
        guest_only = False
        try:
            guest_only = settings.OHAIKIT_GUEST_ONLY
        except AttributeError:
            pass
        if guest_only and not request.session.has_key("bypass_login"):
            login_as_guest(request, True)
            return view_function(request, *args, **kwargs)
        elif not request.user.is_authenticated() and \
           request.session.has_key("bypass_login"):
            return view_function(request, *args, **kwargs)
        else:
            # redirect to login page
            return HttpResponseRedirect("/")
    return wrapped_view


def login_as_guest(request, guest_only_mode=False):
    """
    This function isn't a view, but rather it sets the session
    variables to the guest defaults.
    """
    request.session.set_expiry(0)
    request.session["bypass_login"] = True
    request.session["touch_emulation"] = False
    if guest_only_mode:
        request.session["guest_only_mode"] = True
    return request
    

def controlled_view(view_function, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Replacement for the @login_required decorator that also takes in
    account for if the session is an anonymous one.
    """
    def wrapped_view(request, *args, **kwargs):
        try:
            # In the event that the site is set up to be guest only,
            # automatically create the session without prompting, and
            # set an additional session variable to indicate that
            # things like the logout button doesn't need to displayed.
            # Otherwise, continue as normal.
            if not request.user.is_authenticated() and \
               settings.OHAIKIT_GUEST_ONLY:
                login_as_guest(request, True)
        except AttributeError:
            pass
        if request.user.is_authenticated() or \
           request.session.has_key("bypass_login"):
            return view_function(request, *args, **kwargs)
        else:
            # redirect to login page
            return trigger_login_redirect(request, redirect_field_name, login_url)    
    return wrapped_view


def guest_access(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    This view sets up a guest session and then redirects to wherever.
    The session is set to expire when the browser closes, prompting
    the login page next time they visit the site.
    """
    login_as_guest(request)
    return HttpResponseRedirect(request.POST[redirect_field_name])


def worker_access(request, *args, **kargs):
    """
    Wraps django.contrib.auth.views.login, so that some default
    session values can be added for workrs.
    """
    response = __login(request, *args, **kargs)
    if request.user.is_authenticated():
        request.session.set_expiry(0)
        request.session["touch_emulation"] = True
        if request.session.has_key("bypass_login"):
            del request.session["bypass_login"]
    return response


def session_settings(request):
    """This view serves the page to override the default session
    variables.  Currently, that means enabling/disabling touch screen
    emulation.  If this view is called as a post, it will update the
    settings and redirect to the dashboard."""

    if request.POST:
        request.session["touch_emulation"] = request.POST.has_key("touch_emulation")
        return HttpResponseRedirect(reverse("ohai_kit:index"))
    else:
        context = {
            "touch_emulation" : False,
            "user" : request.user,
            "is_guest" : request.session.has_key("bypass_login"),
            "guest_only" : request.session.has_key("guest_only_mode"),
            "touch_setting" : request.session.get("touch_emulation"),
        }
        return render(request, "ohai_kit/session_settings.html", context)


@controlled_view
def system_index(request):
    """
    The dashboard view is the hub where the user is able to access
    tasks relating to their work, in regards to interacting with
    Project Sets in the system.  Additionally, administrators might
    see employee stats here at some point.
    """

    is_guest = request.session.has_key("bypass_login")

    if is_guest:
        # show only public material (not annotated with css)
        groups = ProjectSet.objects.filter(private=False).order_by("order", "name")
        groups = [i for i in groups if not i.is_empty()]
    elif request.user.is_staff:
        # show everything (annotated with css)
        groups = ProjectSet.objects.all().order_by("order", "name")
    else:
        # show only current material (not annotated with css)
        groups = ProjectSet.objects.filter(legacy=False)
    ungrouped = Project.objects.filter(project_set=None)

    group_count = len(groups)
    if len(ungrouped) > 0:
        group_count += 1

    if group_count == 1:
        if len(groups) == 1:
            return group_view(request, groups[0].slug, True)
        else:
            return group_view(request, None, True)

    group_display = []
    for pset in groups:
        group_display.append({
            "name" : pset.name,
            "url" : reverse("ohai_kit:named_group", args=(pset.slug,)),
            "abstract" : pset.abstract,
            "photo" : pset.photo,
            "special" : False,
            "pk" : pset.pk,
            "legacy" : pset.legacy if request.user.is_staff else False,
            "private" : pset.private if request.user.is_staff else False,
        })
    if len(ungrouped):
        try:
            photo = settings.OHAIKIT_MISC_GROUP_PHOTO
            static_image = True
        except AttributeError:
            photo = None
            static_image = False

        if photo is None:
            static_image = False
            for pset in ungrouped:
                if pset.photo:
                    photo = pset.photo
                    break

        group_display.append({
            "name" : "Miscellaneous",
            "url" : reverse("ohai_kit:misc_group"),
            "abstract" : "Ungrouped Projects",
            "photo" : photo,
            "special" : True,
            "static_image": static_image,
            "legacy" : False,
            "private" : False,
        })

    context = {
        "groups" : group_display,
        "user" : request.user,
        "is_guest" : is_guest,
        "guest_only" : request.session.has_key("guest_only_mode"),
        "touch_emulation" : request.session.get("touch_emulation"),
        }
    return render(request, "ohai_kit/dashboard.html", context)


@controlled_view
def group_view(request, group_slug=None, no_breadcrumbs=False):
    """
    The Group view shows all of the projects for the given group, or
    all of the projects not within groups if group_slug is None.
    """
    projects = None
    if group_slug:
        group = get_object_or_404(ProjectSet, slug=group_slug)
        name = group.name
        projects = group.projects.all().order_by("order", "name")
    else:
        name = "Miscellaneous"
        group = None
        projects = Project.objects.filter(project_set=None)

    context = {
        "projects" : projects,
        "group" : group,
        "group_name" : name,
        "user" : request.user,
        "is_guest" : request.session.has_key("bypass_login"),
        "guest_only" : request.session.has_key("guest_only_mode"),
        "touch_emulation" : request.session.get("touch_emulation"),
        "no_breadcrumbs" : no_breadcrumbs,
        }
    return render(request, "ohai_kit/projectset_view.html", context)


@controlled_view
def ungrouped_view(request):
    return group_view(request)
        

@controlled_view
def project_view(request, project_slug):
    """
    The Project view does different things for different people.  An
    administrator (eventually) should be able to edit Projects via the
    project view rather than the admin page.  For regular users, this
    will be where they begin a workflow.  If the user is a guest user,
    this should redirect right to the workflow view without a bound job.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse("ohai_kit:guest_workflow", args=(project_slug,)))

    user = request.user
    project = get_object_or_404(Project, slug=project_slug)
    active_job = get_active_jobs(user, project)

    if active_job:
        return HttpResponseRedirect(
            reverse("ohai_kit:job_status", args=(active_job.id,)))
    
    context = {
        "user" : user,
        "project" : project,
        "touch_emulation" : False,
        }

    return render(request, "ohai_kit/project_detail.html", context)


@guest_only
def guest_workflow(request, project_slug):
    """
    This view should facilitate the project workflow for guests.
    """
    project = get_object_or_404(Project, slug=project_slug)
    sequence = [[step, "pending"] for step in
                project.workstep_set.order_by("sequence_number")]
    if len(sequence) > 0:
        # make the first step "active"
        sequence[0][1] = "active"

        # the following is to facilitate the navigation buttons without
        # javascript in guest mode
        counter = 1
        for step in sequence:
            this_step = "step_{0}".format(counter)
            next_step = "step_{0}".format(counter+1)
            last_step = "step_{0}".format(counter-1)
            step.append(this_step)
            step.append(next_step)
            step.append(last_step)
            counter+=1
        sequence[0][4] = "step_1"
        sequence[-1][3] = "takemehome"
        
    context = {
        "user": request.user,
        "project": project,
        "is_guest" : True,
        "guest_only" : request.session.has_key("guest_only_mode"),
        "job_id": "-1",
        "sequence": sequence,
        "touch_emulation" : request.session.get("touch_emulation"),
    }
    return render(request, "ohai_kit/workflow.html", context)


@login_required
def job_status(request, job_id):
    """
    This view should facilitate the project workflow for the current
    job.
    """
    job = get_object_or_404(JobInstance, pk=job_id)
    # FIXME assert that the current user is either staff or the user listed
    # on the job
    assert request.user == job.user

    context = {
        "user": request.user,
        "project": job.project,
        "is_guest" : False,
        "guest_only" : request.session.has_key("guest_only_mode"),
        "job_id": job.pk,
        "sequence": job.get_work_sequence(),
        "touch_emulation" : request.session.get("touch_emulation"),
    }
    return render(request, "ohai_kit/workflow.html", context)


@login_required
def start_job(request, project_slug):
    """
    The user is redirected here to initiate a new JobInstance.
    """
    project = get_object_or_404(Project, slug=project_slug)
    job = get_active_jobs(request.user, project)
    if not job:
        job = JobInstance()
        job.project = project
        job.user = request.user
        job.start_time = timezone.now()
        job.batch = "unknown"
        job.save()

    return HttpResponseRedirect(
        reverse("ohai_kit:job_status", args=(job.id,)))


@login_required
def close_job(request, job_id):
    """
    When the user has completed all of the step checks for a given
    job, they should be shown a "close job" button that redirects
    here.
    """
    job = get_object_or_404(JobInstance, pk=job_id)
    # FIXME assert that the current user is either staff or the user listed
    # on the job
    assert request.user == job.user
    if job.completed() and not job.completion_time:
        job.completion_time = timezone.now()
        job.save()

    if job.completed():
        return HttpResponseRedirect(reverse("ohai_kit:index"))
    else:
        return HttpResponseRedirect(
            reverse("ohai_kit:job_status", args=(job_id,)))


@login_required
def update_job(request, job_id):
    """
    The tracker is not to be interacted with via humans, but
    rather is called via XHR from javascript to note job progress
    """
    job = JobInstance.objects.get(id=job_id)
    work_step = WorkStep.objects.get(id=int(request.POST["step_id"]))
    try:
        # if this works, its probably an error, so just ignore it
        receipt = WorkReceipt.objects.get(job=job, step=work_step)
    except WorkReceipt.DoesNotExist:
        # otherwise, create the receipt!
        receipt = WorkReceipt()
        receipt.job = job
        receipt.step = work_step
        receipt.completion_time = timezone.now()
        receipt.save()

    return HttpResponse("OK", content_type="text/plain")
