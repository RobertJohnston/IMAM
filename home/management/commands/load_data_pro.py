from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings

from load_data import rename_cols, merge_in_and_outpatients

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load PROGRAM dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/pro.xlsx').parse('Runs')

        # to speed up testing take only first 30 lines
        #df = df[0:30]

        # Rename all the columns in the imported data
        rename_cols(df)

        # Merge separate inpatients and outpatients variable into one variable / column
        merge_in_and_outpatients(df)

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

        df2 = df.reindex(columns=columnsTitles)
        # df2.set_index(['unique'], inplace=True)

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('program', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE program ADD PRIMARY KEY (urn, first_seen);')
                # add time zones with same code
                print("Program data added.")
        # Imports data with no column names


        except KeyboardInterrupt:
            print("load of registration data failed - db exists already.")
            # when using if_exists='replace' then all column names are deleted
            # when using  if_exists='append' then all column names are maintained, but repeat migrations cause duplicates

        self.stdout.write("Completed")

