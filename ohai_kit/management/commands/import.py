from os.path import isfile

from django.core.management.base import BaseCommand, CommandError
from ohai_kit.models import Project, JobInstance, WorkStep, WorkReceipt

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
        assert isfile(backup_path)
        
        self.stdout.write("import stub")
