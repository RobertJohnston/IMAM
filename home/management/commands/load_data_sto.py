from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings
from load_data import rename_cols, merge_in_and_outpatients

# to run python manage.py load_data

# STOCKS data

class Command(BaseCommand):
    help = 'Loads stock data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load STOCKS dataframe
        # note for STOCKS - use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/sto.xlsx').parse('Runs')

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
                         'self_report',
                         'sto_siteid',
                         'sto_type',
                         'type',
                         'rutf_in',
                         'rutf_used_carton',
                         'rutf_used_sachet',
                         'rutf_bal_carton',
                         'rutf_bal_sachet'
                         'rutf_out',
                         'rutf_bal',
                         'f75_bal_carton',
                         'f75_bal_sachet',
                         'f100_bal_carton'
                         'f100_bal_sachet'

                         'confirm',
                         'unique']

        dataframe.rename(columns={'Self Report (Value) - IMAM Stock ': 'self_report'}, inplace=True)
        dataframe.rename(columns={'StoSiteID (Value) - IMAM Stock ': 'sto_siteid'}, inplace=True)
        dataframe.rename(columns={'StoType (Category) - IMAM Stock ': 'sto_type'}, inplace=True)
        dataframe.rename(columns={'route_by_type (Category) - IMAM Stock ': 'type'}, inplace=True)
        dataframe.rename(columns={'RUTF_in (Value) - IMAM *': 'rutf_in'}, inplace=True)
        # Outpatients
        dataframe.rename(columns={'RUTF_used_carton (Value) - IMAM *': 'rutf_used_carton'}, inplace=True)
        dataframe.rename(columns={'RUTF_used_sachet (Value) - IMAM *': 'rutf_used_sachet'}, inplace=True)
        dataframe.rename(columns={'RUTF_bal_carton (Value) - IMAM *': 'rutf_bal_carton'}, inplace=True)
        dataframe.rename(columns={'RUTF_bal_sachet (Value) - IMAM *': 'rutf_bal_sachet'}, inplace=True)
        # Inpatients
        dataframe.rename(columns={'F75_bal_carton (Value) *': 'f75_bal_carton'}, inplace=True)
        dataframe.rename(columns={'F75_bal_sachet (Value) *': 'f75_bal_sachet'}, inplace=True)
        dataframe.rename(columns={'F100_bal_carton (Value) *': 'f100_bal_carton'}, inplace=True)
        dataframe.rename(columns={'F100_bal_sachet (Value) *': 'f100_bal_sachet'}, inplace=True)
        # LGA database
        dataframe.rename(columns={'RUTF_out (Value) - IMAM *': 'rutf_out'}, inplace=True)
        dataframe.rename(columns={'RUTF_bal (Value) - IMAM *': 'rutf_bal'}, inplace=True)


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




        df2 = df.reindex(columns=columnsTitles)
        # df2.set_index(['unique'], inplace=True)

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

