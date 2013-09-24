from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from ohai_kit.models import Project, JobInstance, \
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




@login_required
def system_index(request):
    """
    The dashboard view is the hub where the user is able to access
    tasks relating to their work, in regards to interacting with
    Projects in the system.  Additionally, administrators might see
    employee stats here at some point.
    """
    projects = Project.objects.all().order_by("name")
    context = {
        "projects" : projects,
        "user" : request.user,
        }
    return render(request, "ohai_kit/dashboard.html", context)


@login_required
def project_view(request, project_id):
    """
    The Project view does different things for different people.  An
    administrator (eventually) should be able to edit Projects via the
    project view rather than the admin page.  For regular users, this
    will be where they begin a workflow.
    """

    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    active_job = get_active_jobs(user, project)

    if active_job:
        return HttpResponseRedirect(
            reverse("ohai_kit:job_status", args=(active_job.id,)))
    
    context = {
        "user" : user,
        "project" : project,
        }

    return render(request, "ohai_kit/project_detail.html", context)


@login_required
def start_job(request, project_id):
    """
    The user is redirected here to initiate a new JobInstance.
    """
    project = get_object_or_404(Project, pk=project_id)
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
        "job_id": job.pk,
        "sequence": job.get_work_sequence(),
        }
    return render(request, "ohai_kit/workflow.html", context)


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
