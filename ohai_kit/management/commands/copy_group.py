from django.core.management.base import BaseCommand, CommandError
from ohai_kit.models import *


class Command(BaseCommand):
    args = ''
    help = """
    This command copies one project set into another.
    """

    def handle(self, *args, **options):
        try:
            src_name = args[0]
            new_name = args[1]
        except IndexError:
            self.stdout.write("Incorrect # of args (src_group, dest_group).")

        src_set = ProjectSet.objects.get(name=src_name)
        try:
            new_set = ProjectSet.objects.get(name=new_name)
        except:
            new_set = None
        assert new_set is None

        new_set = ProjectSet()
        new_set.name = new_name
        new_set.abstract = src_set.abstract
        new_set.photo = src_set.photo
        new_set.order = src_set.order
        new_set.legacy = src_set.legacy
        new_set.private = src_set.private
        new_set.index_mode = src_set.index_mode
        new_set.save()
        
        for src_project in src_set.projects.all():        
            project = Project()
            project.name = src_project.name
            project.abstract = src_project.abstract
            project.photo = src_project.photo
            project.order = src_project.order
            project.save()
            new_set.projects.add(project)

            for src_step in src_project.workstep_set.all():
                step = WorkStep()
                step.project = project
                step.name = src_step.name
                step.description = src_step.description
                step.sequence_number = src_step.sequence_number
                step.save()

                for src_pic in src_step.steppicture_set.all():
                    pic = StepPicture()
                    pic.step = step
                    pic.photo = src_pic.photo
                    pic.caption = src_pic.caption
                    pic.image_order = src_pic.image_order
                    pic.save()

                for src_att in src_step.stepattachment_set.all():
                    att = StepAttachment()
                    att.step = step
                    att.attachment = src_att.attachment
                    att.thumbnail = src_att.thumbnail
                    att.caption = src_att.caption
                    att.order = src_att.order
                    att.save()

                for src_check in src_step.stepcheck_set.all():
                    check = StepCheck()
                    check.step = step
                    check.message = src_check.message
                    check.check_order = src_check.check_order
                    check.save()

        self.stdout.write("Finished copying project set.")
