import json
from home.models import JsonStock, RawStock

from django.core.management.base import BaseCommand
from django.db import transaction

# create model for RawStock

class Command(BaseCommand):
    help = 'Loads program data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        with transaction.atomic():
            a = JsonStock.objects.all().count()
            for json_stock_row in JsonStock.objects.all():
                a -= 1
                api_data = json.loads(json_stock_row.json)

                # No testing needed for update / create
                # by providing an index here, we don't need to get the existing object in the database to update.
                stock_data = RawStock()
                stock_data.id =  json_stock_row.id
                stock_data.name = api_data['contact']['name']

                # Custom data entry for supervision program reports
                # if there is an entry in Protype (True) then supervisor sent data for implementation site
                if json_data['values']['stositeid']['value']:
                    raw_stock.type = json_data['values']['stotype']['category']
                    raw_stock.siteid = json_data['values']['stositeid']['value']


                # Data errors to detect
                # Double entry of stocks - cartons = sachets * 150
                # Entry of confirmed excessive numbers
                # Entry of decimal points


                stock_data.first_seen =  json_stock_row.created_on
                stock_data.last_seen =  json_stock_row.modified_on

                stock_data.save()
                print("count-%s  name-%s" % (a, stock_data.name))

             # bulk insert could be an option





