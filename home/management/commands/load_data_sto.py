from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings
from load_data import rename_cols, merge_in_and_outpatients, create_unique_key

# STOCKS data
# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads stock data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load STOCKS dataframe
        # note for STOCKS - use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/sto.xlsx').parse('Runs')

        # Rename all the columns in the imported data
        rename_cols(df)

        #create_unique_key(df)

        # Create primary key for lga data
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
                         'self_report',
                         'sto_siteid',
                         'sto_type',
                         'type',
                         'rutf_in',
                         'rutf_out',
                         'rutf_bal',
                         'rutf_used_carton',
                         'rutf_used_sachet',
                         'rutf_bal_carton',
                         'rutf_bal_sachet'
                         'f75_bal_carton',
                         'f75_bal_sachet',
                         'f100_bal_carton',
                         'f100_bal_sachet',
                         'confirm',
                         'unique']


        df2 = df.reindex(columns=columnsTitles)
        # df2.set_index(['unique'], inplace=True)


# Imported data is in this format / order

#         u'PostLevel (Category) - IMAM Stock ',
#         u'PostLevel (Value) - IMAM Stock ',
#         u'PostLevel (Text) - IMAM Stock ',
#         u'Self Report (Category) - IMAM Stock ',
#         u'Self Report (Value) - IMAM Stock ',
#         u'Self Report (Text) - IMAM Stock ',
#         u'WeekNum (Category) - IMAM Stock ',
#         u'WeekNum (Value) - IMAM Stock ',
#         u'WeekNum (Text) - IMAM Stock ',
#         u'route_by_level (Category) - IMAM Stock ',
#         u'route_by_level (Value) - IMAM Stock ',
#         u'route_by_level (Text) - IMAM Stock ',
#         u'StoSiteID (Category) - IMAM Stock ',
#         u'StoSiteID (Value) - IMAM Stock ',
#         u'StoSiteID (Text) - IMAM Stock ',
#         u'route_by_type (Category) - IMAM Stock ',
#         u'route_by_type (Value) - IMAM Stock ',
#         u'route_by_type (Text) - IMAM Stock ',
#         u'RUTF_in (Category) - IMAM Stock ',
#         u'RUTF_in (Value) - IMAM Stock ',
#         u'RUTF_in (Text) - IMAM Stock ',
#         u'StoType (Category) - IMAM Stock ',
#         u'StoType (Value) - IMAM Stock ',
#         u'StoType (Text) - IMAM Stock ',
#         u'RUTF_used_carton (Category) - IMAM Stock ',
#         u'RUTF_used_carton (Value) - IMAM Stock ',
#         u'RUTF_used_carton (Text) - IMAM Stock ',
#         u'RUTF_used_sachet (Category) - IMAM Stock ',
#         u'RUTF_used_sachet (Value) - IMAM Stock ',
#         u'RUTF_used_sachet (Text) - IMAM Stock ',
#         u'RUTF_bal_carton (Category) - IMAM Stock ',
#         u'RUTF_bal_carton (Value) - IMAM Stock ',
#         u'RUTF_bal_carton (Text) - IMAM Stock ',
#         u'RUTF_bal_sachet (Category) - IMAM Stock ',
#         u'RUTF_bal_sachet (Value) - IMAM Stock ',
#         u'RUTF_bal_sachet (Text) - IMAM Stock ',
#         u'Confirm (Category) - IMAM Stock ',
#         u'Confirm (Value) - IMAM Stock ',
#         u'Confirm (Text) - IMAM Stock ',
#         u'F75_bal_carton (Category) - IMAM Stock ',
#         u'F75_bal_carton (Value) - IMAM Stock ',
#         u'F75_bal_carton (Text) - IMAM Stock ',
#         u'F75_bal_sachet (Category) - IMAM Stock ',
#         u'F75_bal_sachet (Value) - IMAM Stock ',
#         u'F75_bal_sachet (Text) - IMAM Stock ',
#         u'F100_bal_carton (Category) - IMAM Stock ',
#         u'F100_bal_carton (Value) - IMAM Stock ',
#         u'F100_bal_carton (Text) - IMAM Stock ',
#         u'F100_bal_sachet (Category) - IMAM Stock ',
#         u'F100_bal_sachet (Value) - IMAM Stock ',
#         u'F100_bal_sachet (Text) - IMAM Stock ',




        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('stock', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE stock ADD PRIMARY KEY (urn, first_seen);')
                # add time zones with same code
                print("Stock data added.")


        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")

