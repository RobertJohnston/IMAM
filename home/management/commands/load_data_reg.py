from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load Registration dataframe - note for contacts  - use 'Contacts' tab and not 'Runs'
        df = pd.ExcelFile('/home/robert/Downloads/reg.xlsx').parse('Contacts')

        # edit the data in pandas
        df.rename(columns={'Contact UUID': 'contact_uuid'}, inplace=True)
        df.rename(columns={'URN': 'urn'}, inplace=True)
        df.rename(columns={'Name': 'name'}, inplace=True)
        df.rename(columns={'Groups': 'groups'}, inplace=True)
        df.rename(columns={'SiteID': 'siteid'}, inplace=True)
        df.rename(columns={'Type': 'type'}, inplace=True)
        # Need to edit these date time variables to include Time Zone for Postgresql
        df.rename(columns={'First Seen': 'first_seen'}, inplace=True)
        df.rename(columns={'Last Seen': 'last_seen'}, inplace=True)
        # change variable name of the following
        df.rename(columns={'Mail (Value) - IMAM Register': 'mail'}, inplace=True)
        df.rename(columns={'Post_imp (Value) - IMAM Register': 'post'}, inplace=True)
        # Change the order (the index) of the columns
        columnsTitles = ['contact_uuid', 'urn', 'name', 'groups', 'siteid', 'type', 'first_seen', 'last_seen', 'post',
                         'mail']
        df2 = df.reindex(columns=columnsTitles)
        # set primary key
        df2.set_index('urn')

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('registration', engine, schema='public', if_exists='replace')
            # when using if_exists='replace' then all column names are deleted
            # when using  if_exists='append' then all column names are maintained, but repeat migrations cause duplicates
            with engine.connect() as con:
                con.execute('ALTER TABLE registration ADD PRIMARY KEY (urn);')
                # add time zones with same code
                print("registration data added.")

        # KeyboardInterrupt - will likely never return an exception
        except KeyboardInterrupt:
            print("load of registration data failed - db exists already.")

        self.stdout.write("Completed")
