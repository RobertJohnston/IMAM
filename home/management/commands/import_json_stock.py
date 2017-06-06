import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonStock, LastUpdatedAPICall

# Flow uuid from RapidPro
stock_uuid = "a678268d-0e42-43f1-82cd-aa12117d145d"

class Command(BaseCommand):
    help = 'Loads stock data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        token = open('token').read().strip()
        api_base_url = "https://rapidpro.io"

        page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % stock_uuid
        a = 0

        while page_url_to_process:
            with transaction.atomic():

                response = requests.get(page_url_to_process, headers={"Authorization": "Token %s" % token})

                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_stock in response.json()['results']:
                    id = api_stock['id']
                    print("id %s  count %s" % (id, a))
                    a += 1

                    if JsonStock.objects.filter(id=id):
                        in_db_stock = JsonStock.objects.get(id=id)
                    else:
                        in_db_stock = JsonStock()
                        in_db_stock.id = id

                    in_db_stock.json = json.dumps(api_stock, indent=4)
                    in_db_stock.save()

                page_url_to_process = response.json()['next']
                # print(page_url_to_process)




