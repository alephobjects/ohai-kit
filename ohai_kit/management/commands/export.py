from os.path import isfile
from zipfile import ZipFile
import json
from django.core.management.base import BaseCommand, CommandError
from ohai_kit.models import Project, WorkStep, StepPicture, StepCheck


class Command(BaseCommand):
    args = ''
    help = """
    This command dumps all project information into json files, copy
    over all related pictures, and wraps it all up neatly in a nice
    zip file.
    """

    def handle(self, *args, **options):
        try:
            out_file = args[0]
        except IndexError:
            self.stdout.write(
                "No outfile specified, defaulting to ohai_backups.zip")
            out_file = "ohai_backups.zip"
        if isfile(out_file):
            self.stdout("File exists {0} - doing nothing!".format(out_file))
        
        # First, fetch and cache all textual data and photos.
        # Sequence numbers won't be stored but will determine the
        # order in which records are stored.  They will be regenerated
        # on inport later on.

        data = []
        photos = set()
        for project in Project.objects.all():
            record = {
                "name" : project.name,
                "abstract" : project.abstract,
                "photo" : str(project.photo),
                "steps" : []
            }
            photos.add(project.photo)

            for work_step in project.workstep_set.order_by("sequence_number"):
                step_record = {
                    "name" : work_step.name,
                    "description" : work_step.description,
                    "checks" : [],
                    "photos" : [],
                }

                for check in work_step.stepcheck_set.order_by("check_order"):
                    step_record["checks"].append(check.message)
                
                for img in work_step.steppicture_set.order_by("image_order"):
                    step_record["photos"].append({
                        "path" : str(img.photo),
                        "caption" : img.caption,
                    })
                    photos.add(img.photo)
                record["steps"].append(step_record)
            data.append(record)

        # OK, textual data and photos have been cached, now save them
        # somewhere:

        with ZipFile(out_file, 'w') as target:
            target.writestr("project_data.json", json.dumps(data))
            for photo in photos:
                try:
                    target.write(photo.path, str(photo))
                except OSError:
                    self.stdout.write(
                        "Skipping missing image: ".format(photo.path))
        self.stdout.write("Backup saved to: {0}!".format(out_file))
