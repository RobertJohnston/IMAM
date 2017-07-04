import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonStock, LastUpdatedAPICall
from datetime import datetime
from django.conf import settings

from home.utilities import exception_to_sentry

# Flow uuid from RapidPro
# stock_uuid = "a678268d-0e42-43f1-82cd-aa12117d145d"

class Command(BaseCommand):
    help = 'Loads stock data into JSON format from API'

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
            # api_base_url = "https://rapidpro.io"
            api_base_url = settings.API_BASE_URL

            last_update_time = LastUpdatedAPICall.objects.filter(kind="json_stock").first()

            # Code below is explicitly describing all possible four conditions.
            if options['all'] and last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.STOCK_UUID
                JsonStock.objects.all().delete()

            elif options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.STOCK_UUID
                JsonStock.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_stock")

            elif not options['all'] and last_update_time:
                # Start from end of last api call: GET all data since timestamp of last API call
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s&after=%s" % (
                    settings.STOCK_UUID,
                    # pass timestamp to RapidPro in time format with T between date and time
                    last_update_time.timestamp.strftime("%FT%X.000"),
                )

            elif not options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % settings.STOCK_UUID
                JsonStock.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_stock")

            last_update_time.timestamp = datetime.now()

            a = 0

            while page_url_to_process:

                response = requests.get(page_url_to_process, headers={"Authorization": "Token %s" % token})

                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_stock in response.json()['results']:
                    id = api_stock['id']
                    print("Json Stock %s  id %s" % (a, id))
                    a += 1

                    if JsonStock.objects.filter(id=id):
                        in_db_stock = JsonStock.objects.get(id=id)
                    else:
                        in_db_stock = JsonStock()
                        in_db_stock.id = id

                    # if the data in api_stock matches the data in postgres, then skip
                    if in_db_stock.json == json.dumps(api_stock, indent=4):
                        continue

                    in_db_stock.json = json.dumps(api_stock, indent=4)
                    in_db_stock.save()

                page_url_to_process = response.json()['next']

        last_update_time.save()