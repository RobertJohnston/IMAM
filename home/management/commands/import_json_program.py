import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonProgram, LastUpdatedAPICall

program_uuid = "a9eed2f3-a92c-48dd-aa10-4f139b1171a4"

class Command(BaseCommand):
    help = 'Imports program data into JSON format from API'

    # A command must define handle
    def handle(self, *args, **options):
        token = open('token').read().strip()
        api_base_url = "https://rapidpro.io"

        page_url_to_process = api_base_url + "/api/v2/runs.json?flow=%s" % program_uuid
        a = 0

        while page_url_to_process:
            with transaction.atomic():

                response = requests.get(page_url_to_process, headers={"Authorization": "Token %s" % token})
                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_program in response.json()['results']:
                    id = api_program['id']
                    print("id %s  count %s" %(id, a))
                    a +=1

                    if JsonProgram.objects.filter(id=id):
                        in_db_program = JsonProgram.objects.get(id=id)
                    else:
                        in_db_program = JsonProgram()
                        in_db_program.id = id

                    in_db_program.json = json.dumps(api_program, indent=4)
                    in_db_program.save()

                page_url_to_process = response.json()['next']




