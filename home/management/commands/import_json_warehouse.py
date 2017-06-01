import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonWarehouse, LastUpdatedAPICall

# Be specific about setting path
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads warehouse data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        token = open('token').read().strip()
        api_base_url = "https://rapidpro.io"


        page_url_to_process = api_base_url + "/api/v2/runs.json?"

        while page_url_to_process:
            # with transaction atomic here, there is a commit for each batch from API call
            with transaction.atomic():

                response = requests.get(page_url_to_process + "&flow=%s" % settings.WAREHOUSE_UUID, headers={"Authorization": "Token %s" % token})

                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_warehouse in response.json()['results']:
                    id = api_warehouse['id']
                    print(id)

                    if JsonWarehouse.objects.filter(id=id):
                        in_db_warehouse = JsonWarehouse.objects.get(id=id)
                    else:
                        in_db_warehouse = JsonWarehouse()
                        in_db_warehouse.id = id

                    in_db_warehouse.json = json.dumps(api_warehouse, indent=4)
                    in_db_warehouse.save()

                page_url_to_process = response.json()['next']




