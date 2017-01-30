from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings
from load_data import rename_cols, merge_in_and_outpatients

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads stock data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load PROGRAM dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/sto.xlsx').parse('Runs')

        # to speed up testing take only first 30 lines
        # changed to 1700 to check the stablization center data was merged correctly.
        # df = df[1700:1743]

        # Rename all the columns in the imported data
        rename_cols(df)

        # Create primary key for program data
        df['unique'] =df['urn'].astype(str) + " " + df['first_seen'].astype(object).astype(str)

        # Change the order (the index) of the columns
        columnsTitles = ['contact_uuid',
                         'urn',
                         'name',
                         'groups',
                         'siteid',
                         'first_seen',
                         'last_seen',
                         'weeknum',
                         'role',
                         'type',
                         'prositeid',
                         'protype',
                         'age_group',
                         'beg',
                         'amar',
                         'tin',
                         'dcur',
                         'dead',
                         'defu',
                         'dmed',
                         'tout',
                         'confirm',
                         'unique']

        [u'Contact UUID',
         u'URN',
         u'Name',
         u'Groups',
         u'SiteID',
         u'First Seen',
         u'Last Seen',
         u'PostLevel (Category) - IMAM Stock ',
         u'PostLevel (Value) - IMAM Stock ',
         u'PostLevel (Text) - IMAM Stock ',
         u'Self Report (Category) - IMAM Stock ',
         u'Self Report (Value) - IMAM Stock ',
         u'Self Report (Text) - IMAM Stock ',
         u'WeekNum (Category) - IMAM Stock ',
         u'WeekNum (Value) - IMAM Stock ',
         u'WeekNum (Text) - IMAM Stock ',
         u'route_by_level (Category) - IMAM Stock ',
         u'route_by_level (Value) - IMAM Stock ',
         u'route_by_level (Text) - IMAM Stock ',
         u'StoSiteID (Category) - IMAM Stock ',
         u'StoSiteID (Value) - IMAM Stock ',
         u'StoSiteID (Text) - IMAM Stock ',
         u'route_by_type (Category) - IMAM Stock ',
         u'route_by_type (Value) - IMAM Stock ',
         u'route_by_type (Text) - IMAM Stock ',
         u'RUTF_in (Category) - IMAM Stock ',
         u'RUTF_in (Value) - IMAM Stock ',
         u'RUTF_in (Text) - IMAM Stock ',
         u'StoType (Category) - IMAM Stock ',
         u'StoType (Value) - IMAM Stock ',
         u'StoType (Text) - IMAM Stock ',
         u'RUTF_used_carton (Category) - IMAM Stock ',
         u'RUTF_used_carton (Value) - IMAM Stock ',
         u'RUTF_used_carton (Text) - IMAM Stock ',
         u'RUTF_used_sachet (Category) - IMAM Stock ',
         u'RUTF_used_sachet (Value) - IMAM Stock ',
         u'RUTF_used_sachet (Text) - IMAM Stock ',
         u'RUTF_bal_carton (Category) - IMAM Stock ',
         u'RUTF_bal_carton (Value) - IMAM Stock ',
         u'RUTF_bal_carton (Text) - IMAM Stock ',
         u'RUTF_bal_sachet (Category) - IMAM Stock ',
         u'RUTF_bal_sachet (Value) - IMAM Stock ',
         u'RUTF_bal_sachet (Text) - IMAM Stock ',
         u'Confirm (Category) - IMAM Stock ',
         u'Confirm (Value) - IMAM Stock ',
         u'Confirm (Text) - IMAM Stock ',
         u'F75_bal_carton (Category) - IMAM Stock ',
         u'F75_bal_carton (Value) - IMAM Stock ',
         u'F75_bal_carton (Text) - IMAM Stock ',
         u'F75_bal_sachet (Category) - IMAM Stock ',
         u'F75_bal_sachet (Value) - IMAM Stock ',
         u'F75_bal_sachet (Text) - IMAM Stock ',
         u'F100_bal_carton (Category) - IMAM Stock ',
         u'F100_bal_carton (Value) - IMAM Stock ',
         u'F100_bal_carton (Text) - IMAM Stock ',
         u'F100_bal_sachet (Category) - IMAM Stock ',
         u'F100_bal_sachet (Value) - IMAM Stock ',
         u'F100_bal_sachet (Text) - IMAM Stock ',
         u'RUTFStockAlert (Category) - IMAM Stock ',
         u'RUTFStockAlert (Value) - IMAM Stock ',
         u'RUTFStockAlert (Text) - IMAM Stock ',
         u'F100StockAlert (Category) - IMAM Stock ',
         u'F100StockAlert (Value) - IMAM Stock ',
         u'F100StockAlert (Text) - IMAM Stock ',
         u'F75StockAlert (Category) - IMAM Stock ',
         u'F75StockAlert (Value) - IMAM Stock ',
         u'F75StockAlert (Text) - IMAM Stock ']



        df2 = df.reindex(columns=columnsTitles)
        # df2.set_index(['unique'], inplace=True)

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('program', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE stock ADD PRIMARY KEY (urn, first_seen);')
                # add time zones with same code
                print("Stock data added.")


        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")

