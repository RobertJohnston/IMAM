from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from temba_client.v2 import TembaClient
from isoweek import Week
from home.models import Stock, Registration, LastUpdatedAPICall

from uuid import UUID

# import_stock.py
# to run python manage.py import_stock
# imports data from RapidPro API, cleans data and saves to Postgres

class Command(BaseCommand):
    help = 'Imports stock data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        client = TembaClient('rapidpro.io', open('token').read().strip())

        contact_cache = {x.contact_uuid: x for x in Registration.objects.all()}

        last_update_time = LastUpdatedAPICall.objects.filter(kind="stock").first()

        if last_update_time:
            clients_from_api = client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d', after=last_update_time.timestamp)
        else:
            clients_from_api = client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d')
            last_update_time = LastUpdatedAPICall(kind="stock")

        last_update_time.timestamp = datetime.now()

        a = 0
        # rapidpro expects a uuid to identify flow instead of a flow name
        # https://app.rapidpro.io/flow/editor/a678268d-0e42-43f1-82cd-aa12117d145d/
        for stock_batch in clients_from_api.iterfetches(retry_on_rate_exceed=True):

            with transaction.atomic():
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
                    if Stock.objects.filter(index=stock.id).exists():
                        stock_in_db = Stock.objects.get(index=stock.id)

                    # if id of stock data doesn't exist then create a new row.
                    else:
                        stock_in_db = Stock()
                        stock_in_db.index = stock.id

                    contact = contact_cache[stock.contact.uuid]
                    stock_in_db.contact_uuid = stock.contact.uuid
                    stock_in_db.urn = contact.urn
                    stock_in_db.name = contact.name

                    stock_in_db.siteid = contact.siteid

                    stock_in_db.weeknum = stock.values['weeknum'].value

                    stock_in_db.first_seen = stock.created_on
                    stock_in_db.last_seen =  stock.modified_on

                    # implementation
                    if 'route_by_type' in stock.values:
                        stock_in_db.type = stock.values['route_by_type'].category
                    # supervision
                    elif 'route_by_level' in stock.values:
                        stock_in_db.type = stock.values['stotype'].category
                        stock_in_db.siteid = stock.values['stositeid'].value
                    else:
                        raise Exception()


                    if stock_in_db.type == 'OTP':
                        stock_in_db.rutf_in = stock.values['rutf_in'].value
                        stock_in_db.rutf_used_carton = stock.values['rutf_used_carton'].value
                        stock_in_db.rutf_used_sachet = stock.values['rutf_used_sachet'].value
                        stock_in_db.rutf_bal_carton = stock.values['rutf_bal_carton'].value
                        stock_in_db.rutf_bal_sachet = stock.values['rutf_bal_sachet'].value
                    elif stock_in_db.type == 'SC':
                        # for stabilization center only balance
                        stock_in_db.f100_bal_carton = stock.values['f100_bal_carton'].value
                        stock_in_db.f100_bal_sachet = stock.values['f100_bal_sachet'].value
                        stock_in_db.f75_bal_carton = stock.values['f75_bal_carton'].value
                        stock_in_db.f75_bal_sachet = stock.values['f75_bal_sachet'].value
                    else:
                        raise Exception()




                    # # Introducing Year for X axis
                    stock_in_db.year = stock_in_db.last_seen.isocalendar()[0]
                    last_seen_weeknum = stock_in_db.last_seen.isocalendar()[1]

                    # If report was for weeknum in last year but report data is this year, subtract one year from dataframe.year.
                    # this double conditional identifies the year correctly in the majority of cases
                    # except for reports with weeknum <=44 and more than 8 weeks in past
                    if stock_in_db.weeknum > 44 and last_seen_weeknum < stock_in_db.weeknum:
                        stock_in_db.year -= 1

                    stock_in_db.save()  # Drop duplicates

                    # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                    for oldest_stock_report in Stock.objects.filter(
                        siteid=contact.siteid,
                        year=stock_in_db.year,
                        weeknum=stock_in_db.weeknum,
                        type=stock_in_db.type).order_by('-last_seen')[1:]:

                        print ("     Drop Duplicate")
                        oldest_stock_report.delete()
            
                    a += 1
                    print(a)

        last_update_time.save()