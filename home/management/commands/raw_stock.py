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
        #with transaction.atomic():

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

            last_update_time.timestamp = datetime.now()

            # Countdown ticker
            a = JsonStock.objects.all().count()

            contact_cache = {}
            for contact in Registration.objects.all():
                contact_cache[contact.contact_uuid] = contact



            for json_stock_row in data_to_process.iterator():
                # Use db.reset queries - to avoid excessive memory consumption because django is
                # keeping track of every queries in memory for debugging purpose
                # according to memory_profile commenting out db.reset.queries() doesn't seems to change anything
                # db.reset_queries()

                id = json_stock_row.id
                a -= 1

                print id

                # Update program
                if RawStock.objects.filter(id=id):
                    raw_stock = RawStock.objects.get(id=id)
                    print raw_stock


                # Create contact
                else:
                    raw_stock = RawStock()
                    raw_stock.id = id


            for json_stock_row in data_to_process.iterator():

                id = json_stock_row.id
                a -= 1

                # Update stock
                if RawStock.objects.filter(id=id):
                    raw_stock = RawStock.objects.get(id=id)
                # Create new entry
                else:
                    raw_stock = RawStock()
                    raw_stock.id = id

                # Create api_data from json_stock_row to import to RawStock
                json_data = json.loads(json_stock_row.json)

                if "weeknum" not in json_data['values']:
                    print("Weeknum not in JSON data values for program data entry SKIPPED")
                    # Data entries where Pro was selected but there are no data entered.
                    continue

                # Import contacts
                raw_stock.contact_uuid = json_data['contact']['uuid']

                # This could be related only to weeknum at start of program flow without check for data entry priviledge
                if raw_stock.contact_uuid not in contact_cache:
                    # This is case with someone who has not completed registration but sends initial data
                    continue
                else:
                    contact = contact_cache[raw_stock.contact_uuid]
                    raw_stock.urn = contact.urn


                # Normal data entry for stock reports
                if 'type' in json_data['values']:
                    raw_stock.type = json_data['values']['type']['category']
                    raw_stock.siteid = json_data['values']['siteid']['value']
                # Custom data entry for supervision program reports
                # if there is an entry in Protype (True) then supervisor sent data for implementation site
                elif 'stotype' in json_data['values']:
                    raw_stock.type = json_data['values']['stotype']['category']
                    raw_stock.siteid = json_data['values']['stositeid']['value']
                else:
                    raw_stock.siteid = None
                    raw_stock.type = None

                # OUTPATIENTS
                if raw_stock.type == "OTP" :
                    raw_stock.rutf_in  = json_data['values']['rutf_in ']['value']
                    raw_stock.rutf_used_carton  = json_data['values']['rutf_used_carton ']['value']
                    raw_stock.rutf_used_sachet  = json_data['values']['rutf_used_sachet ']['value']
                    raw_stock.rutf_bal_carton  = json_data['values']['rutf_bal_carton ']['value']
                    raw_stock.rutf_bal_sachet  = json_data['values']['rutf_bal_sachet ']['value']

                # INPATIENTS
                elif raw_stock.type == "SC":
                    raw_stock.f75_bal_carton  = json_data['values']['f75_bal_carton ']['values']
                    raw_stock.f75_bal_sachet  = json_data['values']['f75_bal_sachet ']['values']
                    raw_stock.f100_bal_carton  = json_data['values']['f100_bal_carton ']['values']
                    raw_stock.f100_bal_sachet  = json_data['values']['f100_bal_sachet ']['values']



                # Data errors to detect
                # Double entry of stocks - cartons = sachets * 150
                # Entry of confirmed excessive numbers
                # Entry of decimal points


                raw_stock.first_seen =  json_stock_row.created_on
                raw_stock.last_seen =  json_stock_row.modified_on

                raw_stock.save()
                print("count-%s  name-%s" % (a, raw_stock.name))

             # bulk insert could be an option


            last_update_time.save()
