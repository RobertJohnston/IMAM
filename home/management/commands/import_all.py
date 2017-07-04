from django.core.management.base import BaseCommand
from django.core import management
from home.utilities import exception_to_sentry
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports all data from RapidPro for IMAMbeta'

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):
        reminders_timer = datetime.now()

        management.call_command('import_json_contacts')
        management.call_command('raw_contacts')
        management.call_command('import_contacts2')

        management.call_command('import_json_program')
        management.call_command('raw_program')
        management.call_command('import_program2')

        management.call_command('import_json_stock')
        management.call_command('raw_stock')
        management.call_command('import_stock2')

        management.call_command('import_json_warehouse')
        management.call_command('raw_warehouse')
        management.call_command('import_warehouse2')

        print(datetime.now().strftime('Import_all completed at %d %b %Y %-H:%M:%S'), 'Took %s time to download data' % (datetime.now() - reminders_timer))