import datetime, uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings


filestore = FileSystemStorage(settings.MEDIA_ROOT)

class Project(models.Model):
    """
    A 'Project' is the model in which work steps are keyed against.
    Projects have been refered to as "sub assemblies" in conversation
    so far.
    """

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=lambda:str(uuid.uuid4()))
    abstract = models.TextField()
    photo = models.ImageField(upload_to="uploads", 
                              storage=filestore, blank=True)


class ProjectSet(models.Model):
    """
    A 'ProjectSet' is a set of related projects.  Eg, a ProjectSet may
    encompass all of the different assemblies within a given product.
    The relationship is many2many, for components which may be used in
    multiple products or remain the same accross different product
    versions.
    """

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)
    abstract = models.TextField()
    photo = models.ImageField(upload_to="uploads", 
                              storage=filestore, blank=True)
    projects = models.ManyToManyField(Project, related_name="project_set", blank=True)
    legacy = models.BooleanField(default=False, verbose_name="Discontinued Product")
    private = models.BooleanField(default=False)


class WorkStep(models.Model):
    """
    A 'WorkStep' represents a particual stage in the assembly process.
    """

    def __unicode__(self):
        return self.name

    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    description = models.TextField()
    sequence_number = models.IntegerField(default=0)

    def get_step_pictures(self):
        """
        Returns an ordered list of the associated pictures to this
        step.
        """
        return self.steppicture_set.order_by("image_order")

    def get_step_checks(self):
        """
        returns an ordered list of the associated checks for this
        step.
        """
        return self.stepcheck_set.order_by("check_order")


class StepPicture(models.Model):
    """
    A 'StepPicture' encapsulates a picture associated with a WorkStep.
    """

    step = models.ForeignKey(WorkStep)
    photo = models.ImageField(upload_to="uploads", storage=filestore)
    caption = models.CharField(max_length=500)
    image_order = models.IntegerField(default=0)


class StepCheck(models.Model):
    """
    A 'StepCheck' represents the check boxes that need to be verified
    before the worker may progress to the next step.
    """

    step = models.ForeignKey(WorkStep)
    message = models.CharField(max_length=500)
    check_order = models.IntegerField(default=0)


class JobInstance(models.Model):
    """
    The 'JobInstance' model tracks a user's progress through a given
    project.
    """

    def __unicode__(self):
        return "{0} is building a {1}".format(
            self.user.username, self.project.name)

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    start_time = models.DateTimeField()
    completion_time = models.DateTimeField(blank=True, null=True)
    batch = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    
    pause_total = models.FloatField(blank=True, null=True)
    pause_stamp = models.DateTimeField(blank=True, null=True)

    def get_work_sequence(self):
        """
        Returns a list containing the steps associated with this job,
        and their state according to available work receipts.
        """
        steps = self.project.workstep_set.order_by("sequence_number")
        active_selected = False
        sequence = []
        for step in steps:
            state = "pending"
            try:
                receipt = self.workreceipt_set.get(step__id=step.id)
                state = "completed"
            except WorkReceipt.DoesNotExist:
                if not active_selected:
                    state = "active"
                    active_selected = True
                else:
                    state = "pending"
            sequence.append((step, state))
        return sequence

    def completed(self):
        """
        Returns true if this job has been completed.
        """
        if self.completion_time != None:
            return True
        else:
            steps = self.get_work_sequence()
            for step, state in steps:
                if state != "completed":
                    return False
            return True

    completed.admin_order_field = 'completion_time'
    completed.boolean = True
    completed.short_description = 'Job complete?'

    def get_progress(self):
        """Returns a list illustrating what steps have been completed
        so far, if any."""

        pass

    

class WorkReceipt(models.Model):
    """
    A 'WorkReceipt' tracks when step has been completed within a
    particular 'JobInstance'.
    """

    job = models.ForeignKey(JobInstance)
    step = models.ForeignKey(WorkStep)
    completion_time = models.DateTimeField()
