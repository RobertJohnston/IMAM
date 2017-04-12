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
        for program_batch in client.get_runs(flow=u'IMAM Program').iterfetches(retry_on_rate_exceed=True):

            # Can use these types of calls to fetch data
            # messages = client.get_messages(folder='Inbox').all()
            # fields = client.get_fields().all()
            # but these are very time consuming.  Recommended to use iterfetches as above.

            for program in program_batch:
                if Program.objects.filter(program_uuid=UUID(program.uuid)).exists():
                    program_in_db = Program.objects.get(program_uuid=UUID(program.uuid))
                else:
                    program_in_db = Program()

                program_in_db.uuid = program.uuid
                program_in_db.urn = program.urns[0]
                program_in_db.name = program.name
                program_in_db.groups = program.groups
                program_in_db.siteid = program.fields['siteid']
                program_in_db.first_seen = program.created_on
                program_in_db.last_seen = program.modified_on
                program_in_db.weeknum = program.fields['weeknum']
                program_in_db.type = program.fields['type']
                program_in_db.prositeid = program.fields['prositeid']
                program_in_db.protype = program.fields['protype']
                program_in_db.age_group = program.fields['age_group']
                program_in_db.beg = program.fields['beg_o']
                program_in_db.amar = program.fields['amar_o']
                program_in_db.tin = program.fields['tin_o']
                program_in_db.dcur = program.fields['dcur_o']
                program_in_db.dead = program.fields['dead_o']
                program_in_db.defu = program.fields['defu_o']
                program_in_db.dmed = program.fields['dmed_o']
                program_in_db.confirm = program.fields['confirm']

                program_in_db.save()

                a += 1
                print(a)

# missing amar_i and all other inpatients variables

# Import all data as strings and then clean

# Drop the contacts with siteid = NULL or NaN