from django.core.management.base import BaseCommand
from temba_client.v2 import TembaClient
from home.models import Program

from uuid import UUID

# to run python manage.py import_program


class Command(BaseCommand):
    help = 'Imports program data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        client = TembaClient('rapidpro.io', open('token').read().strip())

        a = 0
        for program_batch in client.get_program(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True):

            # Can use these types of calls to fetch data
            # messages = client.get_messages(folder='Inbox').all()
            # fields = client.get_fields().all()
            # but these are very time consuming.  Recommended to use iterfetches as above.

            for program in program_batch:
                if Program.objects.filter(program_uuid=UUID(program.uuid)).exists():
                    program_in_db = Program.objects.get(program_uuid=UUID(program.uuid))
                else:
                    program_in_db = Program()

                program_in_db.urn = contact.urns[0]
                program_in_db.name = contact.name
                program_in_db.siteid = contact.fields['siteid']
                program_in_db.type = contact.fields['type']
                program_in_db.last_seen = contact.modified_on
                program_in_db.post = contact.fields['VARNAME']

                program_in_db.save()

                a += 1
                print(a)

# Import all data as strings and then clean

# Drop the contacts with siteid = NULL or NaN