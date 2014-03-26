from os.path import isfile
from zipfile import ZipFile
import json
from django.core.management.base import BaseCommand, CommandError
from ohai_kit.models import Project, ProjectSet


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
            self.stdout.write("File exists {0} - doing nothing!".format(out_file))
        
        # First, fetch and cache all textual data and photos.
        # Sequence numbers won't be stored but will determine the
        # order in which records are stored.  They will be regenerated
        # on inport later on.

        data = {
            "projects" : [],
            "groups" : [],
            }
        photos = set()
        
        for group in ProjectSet.objects.all():
            record = {
                "name" : group.name,
                "abstract" : group.abstract,
                "photo" : str(group.photo) or None,
                "projects" : [p.slug for p in group.projects.all()],
                "legacy" : int(group.legacy),
                "private" : int(group.private),
                "index_mode" : int(group.index_mode),
            }
            if record["photo"]:
                photos.add(group.photo)
            data["groups"].append(record)
            
        for project in Project.objects.order_by("order", "name"):
            record = {
                "name" : project.name,
                "slug" : project.slug,
                "abstract" : project.abstract,
                "photo" : str(project.photo) or None,
                "steps" : []
            }
            if record["photo"]:
                photos.add(project.photo)

            for work_step in project.workstep_set.order_by("sequence_number"):
                step_record = {
                    "name" : work_step.name,
                    "description" : work_step.description,
                    "checks" : [],
                    "photos" : [],
                    "attchs" : [],
                }

                for check in work_step.stepcheck_set.order_by("check_order"):
                    step_record["checks"].append(check.message)
                
                for img in work_step.steppicture_set.order_by("image_order"):
                    step_record["photos"].append({
                        "path" : str(img.photo),
                        "caption" : img.caption,
                    })
                    photos.add(img.photo)

                for att in work_step.stepattachment_set.order_by("order"):
                    step_record["attchs"].append({
                        "path" : str(att.attachment),
                        "thumb" : str(att.thumbnail),
                        "caption" : att.caption,
                    })

                record["steps"].append(step_record)
            data["projects"].append(record)

        # OK, textual data and photos have been cached, now save them
        # somewhere:

        with ZipFile(out_file, 'w') as target:
            target.writestr("project_data.json", json.dumps(data))
        self.stdout.write("Backup saved to: {0}!".format(out_file))
