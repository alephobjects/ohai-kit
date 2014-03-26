from os.path import isfile, join
from zipfile import ZipFile
import json
from django.core.management.base import BaseCommand, CommandError
from ohai_kit.models import Project, WorkStep, StepPicture, StepAttachment, StepCheck, ProjectSet
from ohai_kit.models import JobInstance, WorkReceipt
from django.conf import settings


class Command(BaseCommand):
    args = '<backup_path>'
    help = """
    This command overrides existing project definitions etc from the
    data that the corresponding backup command generates.  CAUTION:
    this will delete all work reciepts, and is only intended for
    syncing your public instance with the cannonical internal
    instance!
    """

    def handle(self, *args, **options):
        backup_path = args[0]
        backup = ZipFile(backup_path, 'r')

        # Before deleting or overwritting anything, parse out the
        # saved project data to determine roughly if this archive
        # contains anything we're actually interested in, and record
        # image paths:
        photo_paths = []
        data = json.loads(backup.read("project_data.json"))
        assert len(data) > 0
        assert data.has_key("projects")
        assert data.has_key("groups")
        for project in data["projects"]:
            assert project.has_key("name")
            assert project.has_key("abstract")
            assert project.has_key("photo")
            assert project.has_key("steps")
            photo_paths.append(project["photo"])
            for work_step in project["steps"]:
                for photo in work_step["photos"]:
                    photo_paths.append(photo["path"])

        # That is probably good enough.  Now, let's drop pretty much
        # the entire database!  Nothing could possibly go wrong!
        for model in [Project, WorkStep, StepPicture, StepAttachment,
                      StepCheck, JobInstance, WorkReceipt, ProjectSet]:
            self.stdout.write(
                "Dropping all tables for {0}!".format(str(model)))
            model.objects.all().delete()

        # Now to restore project data and related tables...
        for project in data["projects"]:
            self.stdout.write(
                " - restoring project {0}...".format(project["name"]))
            project_record = Project()
            if project.has_key("slug"):
                project_record.slug = project["slug"]
            project_record.name = project["name"]
            project_record.abstract = project["abstract"]
            project_record.photo = project["photo"]
            project_record.save()

            step_index = 1
            for work_step in project["steps"]:
                step_record = WorkStep()
                step_record.project = project_record
                step_record.name = work_step["name"]
                step_record.description = work_step["description"]
                step_record.sequence_number = step_index*10
                step_record.save()
                step_index += 1
                
                photo_index = 1
                for photo in work_step["photos"]:
                    photo_record = StepPicture()
                    photo_record.step = step_record
                    photo_record.photo = photo["path"]
                    photo_record.caption = photo["caption"]
                    photo_record.image_order = photo_index * 10
                    photo_record.save()
                    photo_index += 1

                if work_step.has_key("attchs"):
                    attachment_index = 1
                    for att in work_step["attchs"]:
                        att_record = StepAttachment()
                        att_record.step = step_record
                        att_record.attachment = att["path"]
                        att_record.caption = att["caption"]
                        att_record.order = attachment_index
                        if att["thumb"]:
                            att_record.thumbnail = att["thumb"]
                        att_record.save()
                        attachment_index += 1

                check_index = 1
                for check in work_step["checks"]:
                    check_record = StepCheck()
                    check_record.step = step_record
                    check_record.message = check
                    check_record.check_order = check_index * 10
                    check_record.save()
                    check_index += 1

        # Restore project set data
        for group in data["groups"]:
            group_record = ProjectSet()
            group_record.name = group["name"]
            group_record.abstract = group["abstract"]
            group_record.photo = group["photo"]
            group_record.legacy = bool(group["legacy"])
            group_record.private = bool(group["private"])
            group_record.save()

            for slug in group["projects"]:
                try:
                    project = Project.objects.get(slug=slug)
                except:
                    self.stdout.write(" ! could not find project for given slug: {0}".format(slug))
                    continue
                group_record.projects.add(project)
            group_record.save()
        
        # All done!
        self.stdout.write("Done!")
