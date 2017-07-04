import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonWarehouse, LastUpdatedAPICall
from datetime import datetime
from django.conf import settings
from home.utilities import exception_to_sentry

class Command(BaseCommand):
    help = 'Loads warehouse data to SQL through API'

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
            api_base_url = settings.API_BASE_URL

            last_update_time = LastUpdatedAPICall.objects.filter(kind="json_warehouse").first()

            # Code below is explicitly describing all possible four conditions.
            if options['all'] and last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.WAREHOUSE_UUID
                JsonWarehouse.objects.all().delete()

            elif options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.WAREHOUSE_UUID
                JsonWarehouse.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_warehouse")

            elif not options['all'] and last_update_time:
                # Start from end of last api call: GET all data since timestamp of last API call
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s&after=%s" % (
                    settings.WAREHOUSE_UUID,
                    # pass timestamp to RapidPro in time format with T between date and time
                    last_update_time.timestamp.strftime("%FT%X.000"),
                )

            elif not options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.WAREHOUSE_UUID
                JsonWarehouse.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_warehouse")

            last_update_time.timestamp = datetime.now()

            a = 0

            while page_url_to_process:

                response = requests.get(page_url_to_process, headers={"Authorization": "Token %s" % token})

                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_warehouse in response.json()['results']:
                    id = api_warehouse['id']
                    print "Json Warehouse %s  id %s" % (a, id)
                    a += 1

                    if JsonWarehouse.objects.filter(id=id):
                        in_db_warehouse = JsonWarehouse.objects.get(id=id)
                    else:
                        in_db_warehouse = JsonWarehouse()
                        in_db_warehouse.id = id

                    # if the data in api_stock matches the data in postgres, then skip
                    if in_db_warehouse.json == json.dumps(api_warehouse, indent=4):
                        continue

                    in_db_warehouse.json = json.dumps(api_warehouse, indent=4)
                    in_db_warehouse.save()

                page_url_to_process = response.json()['next']

            last_update_time.save()

