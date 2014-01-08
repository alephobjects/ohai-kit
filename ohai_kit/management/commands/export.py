from django.core.management.base import BaseCommand, CommandError
from ohai_kit.models import Project, JobInstance, WorkStep, WorkReceipt

class Command(BaseCommand):
    args = ''
    help = """
    This command dumps all project information into json files, copy
    over all related pictures, and wraps it all up neatly in a nice
    zip file.
    """

    def handle(self, *args, **options):
        self.stdout.write("test")
