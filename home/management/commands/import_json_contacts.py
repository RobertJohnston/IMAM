import json
import requests
from urllib import quote
from home.utilities import exception_to_sentry

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import JsonRegistration, LastUpdatedAPICall

# to run python manage.py (name of file), OR
# ipython --pdb manage.py (name of file)


class Command(BaseCommand):
    help = 'Loads registration data to SQL through API'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--all',
    #         action='store_true',
    #         dest='all',
    #         default=False,
    #         help='Import all data',
    #     )

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):
        token = open('token').read().strip()
        api_base_url = "https://rapidpro.io"

        # Check in PostGreSQL database for last timestamp of API call
        # last_update_time = LastUpdatedAPICall.objects.filter(kind="contact").first()
        #
        # Code below is explicitly describing all possible four conditions.
        # T/T   T/F    F/T    F/F
        # if options['all'] and last_update_time:
        #     clients_from_api = client.get_contacts(group='Nut Personnel')
        #
        # elif options['all'] and not last_update_time:
        #     clients_from_api = client.get_contacts(group='Nut Personnel')
        #     last_update_time = LastUpdatedAPICall(kind="contact")
        #
        # elif not options['all'] and last_update_time:
        #     clients_from_api = client.get_contacts(group='Nut Personnel', after=last_update_time.timestamp)
        #
        # elif not options['all'] and not last_update_time:
        #     clients_from_api = client.get_contacts(group='Nut Personnel')
        #     last_update_time = LastUpdatedAPICall(kind="contact")
        #
        # last_update_time.timestamp = datetime.now()
        #
        # a = 0

        page_url_to_process = api_base_url + "/api/v2/contacts.json?"

        while page_url_to_process:
            with transaction.atomic():

                response = requests.get(page_url_to_process + "&group=%s" % quote('Nut Personnel'), headers={"Authorization": "Token %s" % token})
                # Must include Nut Personnel in ?Query to filter for personnel of IMAM program

                assert response.status_code == 200, "%s: %s" % (response.status_code, response.content)

                for api_contact in response.json()['results']:
                    uuid = api_contact['uuid']
                    print(uuid)

                    if JsonRegistration.objects.filter(uuid=uuid):
                        in_db_contact = JsonRegistration.objects.get(uuid=uuid)
                    else:
                        in_db_contact = JsonRegistration()
                        in_db_contact.uuid = uuid

                    in_db_contact.json = json.dumps(api_contact, indent=4)
                    in_db_contact.save()

                page_url_to_process = response.json()['next']