from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from temba_client.v2 import TembaClient
from isoweek import Week
from home.models import Warehouse, Registration, LastUpdatedAPICall

from uuid import UUID


# to run:
#  python manage.py import_warehouse or
#  python manage.py import_warehouse import_warehouse --all

# imports data from RapidPro API, cleans data and saves to Postgres

# 5f2027ce-092f-4712-9b1c-79cddd232fa9


class Command(BaseCommand):
    help = 'Imports warehouse data to SQL through API'

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
        client = TembaClient('rapidpro.io', open('token').read().strip())

        contact_cache = {x.contact_uuid: x for x in Registration.objects.all()}

        last_update_time = LastUpdatedAPICall.objects.filter(kind="warehouse").first()

        # Code below is explicitly describing all possible four conditions.
        # T/T   T/F    F/T    F/F
        if options['all'] and last_update_time:
            clients_from_api = client.get_runs(flow=u'5f2027ce-092f-4712-9b1c-79cddd232fa9')

        elif options['all'] and not last_update_time:
            clients_from_api = client.get_runs(flow=u'5f2027ce-092f-4712-9b1c-79cddd232fa9')
            last_update_time = LastUpdatedAPICall(kind="warehouse")

        elif not options['all'] and last_update_time:
            clients_from_api = client.get_runs(flow=u'5f2027ce-092f-4712-9b1c-79cddd232fa9', after=last_update_time.timestamp)

        elif not options['all'] and not last_update_time:
            clients_from_api = client.get_runs(flow=u'5f2027ce-092f-4712-9b1c-79cddd232fa9')
            last_update_time = LastUpdatedAPICall(kind="warehouse")

        last_update_time.timestamp = datetime.now()

        a = 0

        for stock_batch in clients_from_api.iterfetches(retry_on_rate_exceed=True):

            # with transaction.atomic():
                # Optimization tool - transaction.atomic -is turned off here as it hides errors.

                # the API response is a list in a list
                # to interpret this you have to loop over the content
                for stock in stock_batch:
                    if 'confirm' not in stock.values or stock.values['confirm'].category != 'Yes':
                        print('     Unconfirmed Entry')
                        continue

                    if 'weeknum' not in stock.values:
                        print('     Entry without a weeknum, skip it')
                        continue

                    # if id of stock exists then update the row
                    # Warehouse.id is in the Postgres.  stock.id is in the API
                    if Warehouse.objects.filter(id=stock.id).exists():
                        stock_in_db = Warehouse.objects.get(id=stock.id)

                    # if id of stock data doesn't exist then create a new row.
                    else:
                        stock_in_db = Warehouse()
                        stock_in_db.id = stock.id

                    contact = contact_cache[stock.contact.uuid]
                    stock_in_db.contact_uuid = stock.contact.uuid
                    stock_in_db.urn = contact.urn
                    stock_in_db.name = contact.name

                    stock_in_db.siteid = contact.siteid

                    stock_in_db.weeknum = stock.values['weeknum'].value

                    stock_in_db.first_seen = stock.created_on
                    stock_in_db.last_seen = stock.modified_on

                    stock_in_db.rutf_in = stock.values['rutf_in'].value
                    stock_in_db.rutf_out = stock.values['rutf_out'].value
                    stock_in_db.rutf_bal = stock.values['rutf_bal'].value

                    # FIXME
                    #Add data cleaning

                    # if siteid = one of list below then add to import normal stock data not warehouse data
                    # better to identify all siteids > 3699
                    # 3508110034
                    # 3502110031
                    # 3319110014 - error in registration - siteid does not exist
                    # 3301110008
                    # 827110013
                    # 821110053

                    # Introducing Year for X axis
                    # Remember that this code is running in a loop over all data in the api call
                    stock_in_db.year = stock_in_db.last_seen.isocalendar()[0]
                    last_seen_weeknum = stock_in_db.last_seen.isocalendar()[1]

                    # If report was for weeknum in last year but report data is this year, subtract one year from dataframe.year.
                    # this double conditional identifies the year correctly in the majority of cases
                    # except for reports with weeknum <=44 and more than 8 weeks in past
                    if stock_in_db.weeknum > 44 and last_seen_weeknum < stock_in_db.weeknum:
                        stock_in_db.year -= 1

                    stock_in_db.save()  # Drop duplicates

                    # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                    for oldest_stock_report in Warehouse.objects.filter(
                            siteid=contact.siteid,
                            year=stock_in_db.year,
                            weeknum=stock_in_db.weeknum).order_by('-last_seen')[1:]:
                        print("     Drop Duplicate")
                        oldest_stock_report.delete()

                    a += 1
                    print(a)

        last_update_time.save()