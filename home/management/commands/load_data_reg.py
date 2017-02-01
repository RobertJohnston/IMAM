from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

from load_data import rename_cols

# to run python manage.py load_data

# remember to delete the table in PostGresSql before running load or the column names do not appear
# to address this issue, could insert a drop table command in this file below.

class Command(BaseCommand):
    help = 'Loads registration data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Drop table if exists.
        # engine.execute(""" DROP TABLE IF EXISTS "%s" """ % (tablename))

        # Load Registration dataframe - note for contacts  - use 'Contacts' tab and not 'Runs'
        df = pd.ExcelFile('/home/robert/Downloads/reg.xlsx').parse('Contacts')

        # Rename all the columns in the imported data
        rename_cols(df)

        # missing Post_sup column with post for supervision staff.
        # add Post_sup column and convert to post

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

        # drop row if urn is null

        # set primary key
        df2.set_index('urn')

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('registration', engine, schema='public', if_exists='replace')
            # when using if_exists='replace' then all column names are deleted

            with engine.connect() as con:
                con.execute('ALTER TABLE registration ADD PRIMARY KEY (urn);')
                # add time zones with same code
                #con.execute('ALTER TABLE registration ALTER first_seen TYPE timestamptz;')
                #con.execute('ALTER TABLE registration ALTER last_seen TYPE timestamptz;')
                # The lines above save the data with Belgium time zone not Nigeria.
                print("Registration data added.")

        # KeyboardInterrupt - will likely never return an exception
        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")
