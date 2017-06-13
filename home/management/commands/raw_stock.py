import json

from home.models import Registration, JsonStock, RawStock, LastUpdatedAPICall
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime


class Command(BaseCommand):
    help = 'Loads RawStock data from JsonStock'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Import all data',
        )

    # A command must define handle
    def handle(self, *args, **options):
        with transaction.atomic():

            last_update_time = LastUpdatedAPICall.objects.filter(kind="raw_stock").first()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                RawStock.objects.all().delete()
                data_to_process = JsonStock.objects.all()

            elif options['all'] and not last_update_time:
                RawStock.objects.all().delete()
                data_to_process = JsonStock.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_stock")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                data_to_process = JsonStock.objects.filter(modified_on__gte=last_update_time.timestamp)

            elif not options['all'] and not last_update_time:
                RawStock.objects.all().delete()
                data_to_process = JsonStock.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_stock")

            else:
                raise Exception()
                # This is unncessary in this context but good programming practice

            last_update_time.timestamp = datetime.now()

            # Countdown ticker
            counter= JsonStock.objects.all().count()

            contact_cache = {}
            for contact in Registration.objects.all():
                contact_cache[contact.contact_uuid] = contact

            for json_stock_row in data_to_process.iterator():

                id = json_stock_row.id
                counter -= 1

                # Update stock
                if RawStock.objects.filter(id=id):
                    raw_stock = RawStock.objects.get(id=id)
                # Create new entry
                else:
                    raw_stock = RawStock()
                    raw_stock.id = id

                # Create api_data from json_stock_row to import to RawStock
                json_data = json.loads(json_stock_row.json)

                # Import contacts
                raw_stock.contact_uuid = json_data['contact']['uuid']

                # This could be related only to weeknum at start of program flow without check for data entry priviledge
                if raw_stock.contact_uuid not in contact_cache:
                    # This is case with someone who has not completed registration but sends initial data
                    continue
                else:
                    contact = contact_cache[raw_stock.contact_uuid]
                    raw_stock.urn = contact.urn

                raw_stock.name = json_data['contact']['name']

                # Normal data entry for stock reports - in program this is called 'type'
                if 'route_by_type' in json_data['values']:
                    raw_stock.type   = json_data['values']['route_by_type']['category']

                    # raw_stock.siteid = json_data['values']['siteid']['value']

                    # Data stitching to integrate SITEID is working in raw_program since 8th June 2017
                    if 'siteid' in json_data['values'] and isinstance(json_data['values']['siteid']['value'], (int, float)):
                        raw_stock.siteid = json_data['values']['siteid']['value']
                        print raw_stock.siteid
                    # code below brings siteid from contacts for old data entries before the corrections in RapidPro
                    else:
                        raw_stock.siteid = contact.siteid

                # Custom data entry for supervision program reports
                # if there is an entry in Protype (True) then supervisor sent data for implementation site
                elif 'stotype' in json_data['values']:
                    raw_stock.type   = json_data['values']['stotype']['category']
                    raw_stock.siteid = json_data['values']['stositeid']['value'] if 'stositeid' in json_data['values'] else None
                    print("SUPERVISION DATA ENTRY with type %s and siteid %s" % (raw_stock.type, raw_stock.siteid))
                else:
                    raw_stock.siteid = None
                    raw_stock.type = None

                raw_stock.weeknum = json_data['values']['weeknum']['value']  if 'weeknum' in json_data['values'] else None
                # In the RapidPro flow for stock, the collection of weeknum is after the filter for
                # level (implementation or supervision, thus there is no need to include a skip
                # if weeknum is not present

                # OUTPATIENTS
                if raw_stock.type == "OTP" :
                    raw_stock.rutf_in           = json_data['values']['rutf_in']['value']          if 'rutf_in' in json_data['values'] else None
                    raw_stock.rutf_used_carton  = json_data['values']['rutf_used_carton']['value'] if 'rutf_used_carton' in json_data['values'] else None
                    raw_stock.rutf_used_sachet  = json_data['values']['rutf_used_sachet']['value'] if 'rutf_used_sachet' in json_data['values'] else None
                    raw_stock.rutf_bal_carton   = json_data['values']['rutf_bal_carton']['value']  if 'rutf_bal_carton' in json_data['values'] else None
                    raw_stock.rutf_bal_sachet   = json_data['values']['rutf_bal_sachet']['value']  if 'rutf_bal_sachet' in json_data['values'] else None

                # INPATIENTS
                elif raw_stock.type == "SC":
                    raw_stock.f75_bal_carton    = json_data['values']['f75_bal_carton']['value']  if 'f75_bal_carton' in json_data['values'] else None
                    raw_stock.f75_bal_sachet    = json_data['values']['f75_bal_sachet']['value']  if 'f75_bal_sachet' in json_data['values'] else None
                    raw_stock.f100_bal_carton   = json_data['values']['f100_bal_carton']['value'] if 'f100_bal_carton' in json_data['values'] else None
                    raw_stock.f100_bal_sachet   = json_data['values']['f100_bal_sachet']['value'] if 'f100_bal_sachet' in json_data['values'] else None


                # Data errors to detect
                # Double entry of stocks - cartons = sachets * 150
                # Entry of confirmed excessive numbers
                # Entry of decimal points


                raw_stock.first_seen =  json_data['created_on']
                raw_stock.last_seen =  json_data['modified_on']

                if 'confirm' in json_data['values']:
                    raw_stock.confirm = json_data['values']['confirm']['category']

                raw_stock.save()
                print("count %s " % counter)

             # bulk insert could be an option


            last_update_time.save()
