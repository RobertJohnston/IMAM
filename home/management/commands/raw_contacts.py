import json
from home.models import JsonRegistration, RawRegistration, LastUpdatedAPICall
from django.core.management.base import BaseCommand

from django.db import transaction
from datetime import datetime
from home.utilities import exception_to_sentry

# create model for RawRegistration


class Command(BaseCommand):
    help = 'Imports RawRegistration data from JsonRegistration'

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

            last_update_time = LastUpdatedAPICall.objects.filter(kind="raw_contacts").first()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                RawRegistration.objects.all().delete()
                data_to_process = JsonRegistration.objects.all()

            elif options['all'] and not last_update_time:
                RawRegistration.objects.all().delete()
                data_to_process = JsonRegistration.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_contacts")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                data_to_process = JsonRegistration.objects.filter(modified_on__gte=last_update_time.timestamp)

            elif not options['all'] and not last_update_time:
                RawRegistration.objects.all().delete()
                data_to_process = JsonRegistration.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_contacts")

            last_update_time.timestamp = datetime.now()

            # Change to countdown
            counter = JsonRegistration.objects.all().count()

            for json_contact_row in data_to_process.iterator():

                uuid = json_contact_row.uuid
                counter -= 1

                # Create json_data from json_contact_row to import to RawRegistration
                json_data = json.loads(json_contact_row.json)

                # Update contact
                if RawRegistration.objects.filter(uuid=uuid):
                    print("Raw Contacts countdown %s UPDATING a contact for %s with uuid %s" % (counter, json_data['name'].encode("utf-8"), uuid))
                    raw_contacts = RawRegistration.objects.get(uuid=uuid)
                # Create contact
                else:
                    print("Raw Contacts countdown %s    CREATING a contact for %s with uuid %s" % (counter, json_data['name'].encode("utf-8"), uuid))
                    raw_contacts = RawRegistration()
                    raw_contacts.uuid = uuid


                # In 2017 RapidPro added capacity to have several telephone numbers for one contact
                # In Nigeria personnel with two or more telephone numbers are registered on separate rows
                raw_contacts.urn = json_data['urns'][0]
                raw_contacts.name = json_data['name']
                # Data on siteid, type, post and mail are dictionaries in dictionaries in the api data
                raw_contacts.siteid = json_data['fields']['siteid']
                raw_contacts.type = json_data['fields']['type']
                raw_contacts.post = json_data['fields']['post']
                raw_contacts.mail = json_data['fields']['mail']
                raw_contacts.first_seen = json_data['created_on']
                raw_contacts.last_seen = json_data['modified_on']

                raw_contacts.save()

            last_update_time.save()





