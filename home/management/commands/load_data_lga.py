from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings

from load_data import rename_cols, merge_in_and_outpatients, create_unique_key

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

        # create_unique_key(df)

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
                         'rutf_in',
                         'rutf_out',
                         'rutf_bal',
                         'confirm',
                         'unique']

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

