import json
import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonRegistration, LastUpdatedAPICall

from urllib import quote
from datetime import datetime
from home.utilities import exception_to_sentry


class Command(BaseCommand):
    help = 'Loads registration data to SQL through API'

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

            # Check in PostGreSQL database for last timestamp of API call
            last_update_time = LastUpdatedAPICall.objects.filter(kind="json_contact").first()

            # Code below is explicitly describing all possible four conditions.
            # T/T   T/F    F/T    F/F
            if options['all'] and last_update_time:
                page_url_to_process = api_base_url + "/api/v2/contacts.json?group=%s" % quote('Nut Personnel')
                JsonRegistration.objects.all().delete()

            elif options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/contacts.json?group=%s" % quote('Nut Personnel')
                JsonRegistration.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_contact")

            elif not options['all'] and last_update_time:
                page_url_to_process = api_base_url + "/api/v2/contacts.json?group=%s&after=%s" % (
                    quote('Nut Personnel'),
                    last_update_time.timestamp.strftime("%FT%X.000"),
                )

            elif not options['all'] and not last_update_time:
                page_url_to_process = api_base_url + "/api/v2/contacts.json?group=%s" % quote('Nut Personnel')
                JsonRegistration.objects.all().delete()
                last_update_time = LastUpdatedAPICall(kind="json_contact")

            last_update_time.timestamp = datetime.now()

            counter = 0

            while page_url_to_process:

                # print page_url_to_process
                # print page_url to test if the concatenation of http request increases or is replaced at every round
                response = requests.get(page_url_to_process, headers={"Authorization": "Token %s" % token})
                # Must include Nut Personnel in ?Query to filter for personnel of IMAM program
                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_contact in response.json()['results']:
                    uuid = api_contact['uuid']
                    print "Json Contacts %s  UUID %s" %(counter, uuid)
                    counter += 1

                    if JsonRegistration.objects.filter(uuid=uuid):
                        in_db_contact = JsonRegistration.objects.get(uuid=uuid)
                    else:
                        in_db_contact = JsonRegistration()
                        in_db_contact.uuid = uuid

                    in_db_contact.json = json.dumps(api_contact, indent=4)
                    in_db_contact.save()

                page_url_to_process = response.json()['next']

            last_update_time.save()   # The last_update_time should be inside the transaction
