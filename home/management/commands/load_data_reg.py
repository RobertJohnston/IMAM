from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

from load_data import rename_cols, merge_in_and_outpatients

# Registration Data

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads data from xls to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load Registration dataframe - note for contacts  - use 'Contacts' tab and not 'Runs'
        df = pd.ExcelFile('/home/robert/Downloads/reg.xlsx').parse('Contacts')

        # Rename all the columns in the imported data
        rename_cols(df)

        # Change the order (the index) of the columns
        columnsTitles = ['contact_uuid',
                         'urn',
                         'name',
                         'groups',
                         'siteid',
                         'type',
                         'first_seen',
                         'last_seen',
                         'post',
                         'mail']

        df2 = df.reindex(columns=columnsTitles)

        # set primary key - should be urn
        #df.set_index('urn')

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('registration', engine, schema='public', if_exists='replace')

            with engine.connect() as con:
                con.execute('ALTER TABLE registration ADD PRIMARY KEY (contact_uuid);')
                # add time zones with same code
                print("registration data added.")

        # KeyboardInterrupt - will likely never return an exception
        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")
