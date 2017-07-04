import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from home.models import JsonProgram, LastUpdatedAPICall
from datetime import datetime

from home.utilities import exception_to_sentry


class Command(BaseCommand):
    help = 'Imports program data into JSON format from API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Import all data',
        )

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):
        with transaction.atomic():

            token = open('token').read().strip()
            api_base_url = "https://rapidpro.io"

            last_update_time = LastUpdatedAPICall.objects.filter(kind="json_program").first()

            # Code below is explicitly describing all possible four conditions.
            # T/T   T/F    F/T    F/F
            if options['all'] and last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.PROGRAM_UUID
                JsonProgram.objects.all().delete()

            elif options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.PROGRAM_UUID
                JsonProgram.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_program")

            elif not options['all'] and last_update_time:
                # Start from end of last api call: GET all data since timestamp of last API call
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s&after=%s" % (
                    settings.PROGRAM_UUID,
                    last_update_time.timestamp.strftime("%FT%X.000"),
                )

            elif not options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.PROGRAM_UUID
                JsonProgram.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_program")

            last_update_time.timestamp = datetime.now()

            counter = 0

            while page_url_to_process:

                response = requests.get(page_url_to_process, headers={"Authorization": "Token %s" % token})
                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_program in response.json()['results']:
                    id = api_program['id']
                    print("Json Program %s  id %s" %(counter, id))
                    counter +=1

                    if JsonProgram.objects.filter(id=id):
                        in_db_program = JsonProgram.objects.get(id=id)
                    else:
                        in_db_program = JsonProgram()
                        in_db_program.id = id

                    if in_db_program.json == json.dumps(api_program, indent=4):
                        continue

                    in_db_program.json = json.dumps(api_program, indent=4)
                    in_db_program.save()

                page_url_to_process = response.json()['next']

        last_update_time.save()

