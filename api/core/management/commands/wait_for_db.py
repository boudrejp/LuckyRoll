import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django Command to Pause Execution until DB is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB....')
        db_conn = None
        count = 0
        while not db_conn and count < 50:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database Unavailable, waiting 1 second....')
                time.sleep(1)
                count += 1
        self.stdout.write(self.style.SUCCESS("Database Available!"))
