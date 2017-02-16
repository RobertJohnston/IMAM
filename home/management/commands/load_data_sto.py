from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings

from load_data import rename_cols

# to run python manage.py load_data

# STOCKS DATA

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load PROGRAM dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
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
                         'level',
                         'self_report',
                         'sto_siteid',
                         'sto_type',
                         'type',
                         'rutf_in',
                         'rutf_used_carton',
                         'rutf_used_sachet',
                         'rutf_bal_carton',
                         'rutf_bal_sachet',
                         # rutf_out and rutf_bal were not entered into postgres.
                         'rutf_out',
                         'rutf_bal',
                         'f75_bal_carton',
                         'f75_bal_sachet',
                         'f100_bal_carton',
                         'f100_bal_sachet',
                         'confirm',
                         'unique']

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

        # clean data

        # insert cleaned data into postgresql

        self.stdout.write("Completed")

