import json

from home.models import Registration, JsonWarehouse, RawWarehouse, LastUpdatedAPICall
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime
from home.utilities import exception_to_sentry


class Command(BaseCommand):
    help = 'Loads RawWarehouse data from JsonWarehouse'

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

            last_update_time = LastUpdatedAPICall.objects.filter(kind="raw_warehouse").first()

            # Countdown ticker
            counter= JsonWarehouse.objects.all().count()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                RawWarehouse.objects.all().delete()
                data_to_process = JsonWarehouse.objects.all()

            elif options['all'] and not last_update_time:
                RawWarehouse.objects.all().delete()
                data_to_process = JsonWarehouse.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_warehouse")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                data_to_process = JsonWarehouse.objects.filter(modified_on__gte=last_update_time.timestamp)
                # Update counter to only include those entries since last update timestamp
                counter = JsonWarehouse.objects.filter(modified_on__gte=last_update_time.timestamp).count()

            elif not options['all'] and not last_update_time:
                RawWarehouse.objects.all().delete()
                data_to_process = JsonWarehouse.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_warehouse")

            else:
                raise Exception()
                # This is unncessary in this context but good programming practice

            last_update_time.timestamp = datetime.now()

            contact_cache = {}
            for contact in Registration.objects.all():
                contact_cache[contact.contact_uuid] = contact

            for json_row in data_to_process.iterator():

                id = json_row.id
                counter -= 1

                # Update warehouse
                if RawWarehouse.objects.filter(id=id):
                    raw_warehouse = RawWarehouse.objects.get(id=id)
                # Create new entry
                else:
                    raw_warehouse = RawWarehouse()
                    raw_warehouse.id = id

                # Create api_data from json_row to import to RawWarehouse
                json_data = json.loads(json_row.json)

                # Import contacts
                raw_warehouse.contact_uuid = json_data['contact']['uuid']

                # This could be related only to weeknum at start of program flow without check for data entry priviledge
                if raw_warehouse.contact_uuid not in contact_cache:
                    # This is case with someone who has not completed registration but sends initial data
                    continue
                else:
                    contact = contact_cache[raw_warehouse.contact_uuid]
                    raw_warehouse.urn = contact.urn

                raw_warehouse.name = json_data['contact']['name']

                # Data stitching to integrate SITEID is working in raw_program since 8th June 2017
                if 'siteid' in json_data['values'] and isinstance(json_data['values']['siteid']['value'], (int, float)):
                    raw_warehouse.siteid = json_data['values']['siteid']['value']
                    print(raw_warehouse.siteid, "SiteID from RapidPro")
                # code below brings siteid from contacts for old data entries before the corrections in RapidPro
                elif contact.siteid: # if true / exists
                    raw_warehouse.siteid = contact.siteid
                    print(raw_warehouse.siteid, "                     SiteID from Contacts")

                else:
                    raw_warehouse.siteid = None

                raw_warehouse.weeknum = json_data['values']['weeknum']['value']  if 'weeknum' in json_data['values'] else None
                # In the RapidPro flow for warehouse, the collection of weeknum is after the filter for level
                # (implementation or supervision, thus there is no need to include a skip if weeknum is not present

                raw_warehouse.rutf_in  = json_data['values']['rutf_in']['value']  if 'rutf_in' in json_data['values'] else None
                raw_warehouse.rutf_out = json_data['values']['rutf_out']['value'] if 'rutf_out' in json_data['values'] else None
                raw_warehouse.rutf_bal = json_data['values']['rutf_bal']['value'] if 'rutf_bal' in json_data['values'] else None

                # Data errors to detect
                # Double entry of stocks - cartons = sachets * 150
                # Entry of confirmed excessive numbers
                # Entry of decimal points

                raw_warehouse.first_seen =  json_data['created_on']
                raw_warehouse.last_seen =  json_data['modified_on']

                if 'confirm' in json_data['values']:
                    raw_warehouse.confirm = json_data['values']['confirm']['category']

                raw_warehouse.save()
                print("count %s " % counter)

             # bulk insert could be an option


