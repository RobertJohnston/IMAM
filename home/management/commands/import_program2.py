from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from isoweek import Week
from home.models import RawProgram, Program, LastUpdatedAPICall

from uuid import UUID

# import_program.py
# to run python manage.py import_program
# imports program data from RapidPro API, cleans data and saves to Postgres

# Change data entry to accept all data and clean data  after
# 1 -  to import data as JSON
# 2 -  import to Postgres as raw data
# 3 -  do data cleaning as save as clean data

# Currently Data errors such as strings instead of integers are not available
# Other data entry mistakes such as aberrant values are still visible.

class Command(BaseCommand):
    help = 'Import Program data from RawProgram'

    # A command must define handle
    def handle(self, *args, **options):
        with transaction.atomic():
            a = Program.objects.all().count()

            for program_row in RawProgram.objects.all():
                a -= 1

                program_in_db = Program()

                program_in_db.contact_uuid = program_row.contact_uuid
                # URN
                program_in_db.urn = program_row.urn
                # Name
                program_in_db.name = program_row.name




                program_in_db.first_seen = program_row.first_seen
                program_in_db.last_seen = program_row.last_seen

                print("count-%s  Name-%s" %(a, program_in_db.name))
                program_in_db.save()
