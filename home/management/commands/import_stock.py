from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from temba_client.v2 import TembaClient
from isoweek import Week
from home.models import Stock, Registration

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

        a = 0
        # rapidpro expects a uuid to identify flow instead of a flow name
        # https://app.rapidpro.io/flow/editor/a678268d-0e42-43f1-82cd-aa12117d145d/
        for stock_batch in client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d').iterfetches(retry_on_rate_exceed=True):

            # with transaction.atomic():
            # Optimization tool - transaction.atomic -is turned off here as it hides errors.

                # the API response is a list in a list
                # to interpret this you have to loop over the content
                for stock in stock_batch:
                    if 'confirm' not in stock.values or stock.values['confirm'].category != 'Yes':
                        print('     Unconfirmed Entry')
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

                    stock_in_db.first_seen = stock.created_on
                    stock_in_db.last_seen =  stock.modified_on

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