from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings
from load_data import rename_cols, merge_in_and_outpatients

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads LGA and State level stock data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load LGA dataframe
        # note for LGA - use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/lga.xlsx').parse('Runs')

        # Rename all the columns in the imported data
        rename_cols(df)

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
                         'role',
                         'type',

                         'confirm',
                         'unique']

        u'URN',
        u'Name',
        u'Groups',
        u'SiteID',
        u'First Seen',
        u'Last Seen',
        u'WeekNum (Category) - IMAM LGA State Stocks',
        u'WeekNum (Value) - IMAM LGA State Stocks',
        u'WeekNum (Text) - IMAM LGA State Stocks',
        u'RUTF_in (Category) - IMAM LGA State Stocks',
        u'RUTF_in (Value) - IMAM LGA State Stocks',
        u'RUTF_in (Text) - IMAM LGA State Stocks',
        u'RUTF_out (Category) - IMAM LGA State Stocks',
        u'RUTF_out (Value) - IMAM LGA State Stocks',
        u'RUTF_out (Text) - IMAM LGA State Stocks',
        u'RUTF_bal (Category) - IMAM LGA State Stocks',
        u'RUTF_bal (Value) - IMAM LGA State Stocks',
        u'RUTF_bal (Text) - IMAM LGA State Stocks',
        u'confirm (Category) - IMAM LGA State Stocks',
        u'confirm (Value) - IMAM LGA State Stocks',
        u'confirm (Text) - IMAM LGA State Stocks',
        u'Response 6 (Category) - IMAM LGA State Stocks',
        u'Response 6 (Value) - IMAM LGA State Stocks',
        u'Response 6 (Text) - IMAM LGA State Stocks']

        df2 = df.reindex(columns=columnsTitles)
        # df2.set_index(['unique'], inplace=True)

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('lga', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE lga ADD PRIMARY KEY (urn, first_seen);')
                # add time zones with same code
                print("LGA and State stock data added.")


        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")

