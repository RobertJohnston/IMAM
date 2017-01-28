from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

# from polls.models import Question as Poll

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


        # Load PROGRAM dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/pro.xlsx').parse('Runs')

        # edit the data in pandas
        df.rename(columns={'Contact UUID': 'contact_uuid'}, inplace=True)
        df.rename(columns={'URN': 'urn'}, inplace=True)
        df.rename(columns={'Name': 'name'}, inplace=True)
        df.rename(columns={'Groups': 'groups'}, inplace=True)
        df.rename(columns={'SiteID': 'siteid'}, inplace=True)
        # Need to edit these date time variables to include Time Zone for Postgresql
        df.rename(columns={'First Seen': 'first_seen'}, inplace=True)
        df.rename(columns={'Last Seen': 'last_seen'}, inplace=True)
        # df.rename(columns={'Mail (Value) - IMAM Register': 'mail'}, inplace=True)
        # # Mail (Value) - IMAM Register
        # df.rename(columns={'Post_imp (Value) - IMAM Register': 'post'}, inplace=True)
        # # Post_imp (Value) - IMAM Register


        df.rename(columns = {'URN':'urn'}, inplace = True)
        df.rename(columns = {'First Seen':'first_seen'}, inplace = True)
        df.rename(columns = {'Last Seen':'last_seen'}, inplace = True)
        df.rename(columns = {'WeekNum (Value) - IMAM Program':'weeknum'}, inplace = True)
        df.rename(columns = {'Role (Value) - IMAM Program':'role'}, inplace = True)
        df.rename(columns={'Type (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'ProSiteID (Value) - IMAM Program': 'prositeid'}, inplace=True)

        df.rename(columns={'ProType (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'age group (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Beg_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Amar_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Tin_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dcur_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dead_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'DefU_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dmed_o (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Tout_o (Value) - IMAM Program': 'type'}, inplace=True)
        # convert admissions and exits to one column a piece not duplicates for out / in patients
        df.rename(columns={'Beg_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Amar_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Tin_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dcur_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dcur_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dead_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'DefU_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Dmed_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Tout_i (Value) - IMAM Program': 'type'}, inplace=True)
        df.rename(columns={'Confirm (Category) - IMAM Program': 'type'}, inplace=True)


        df['pk'] =df['urn'].astype(str) + " " + df['first_seen'].astype(object).astype(str)

        columnsTitles = ['pk','urn', 'first_seen']
        df2 = df.reindex(columns = columnsTitles)
        df2.set_index(['pk'], inplace=True)






        # Create the unique key
        df['unique'] = df['urn'].astype(str) + " " + df['first_seen'].astype(object).astype(str)

        # Change the order (the index) of the columns
        columnsTitles = ['contact_uuid', 'urn', 'name', 'groups', 'siteid', 'first_seen', 'last_seen', 'unique']
        df2 = df.reindex(columns=columnsTitles)
        df2.set_index('unique')

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df2.to_sql('program', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE program ADD PRIMARY KEY (contact_uuid);')
                # add time zones with same code
                print("Program data added.")
        except KeyboardInterrupt:
            print("load of registration data failed - db exists already.")
            # when using if_exists='replace' then all column names are deleted
            # when using  if_exists='append' then all column names are maintained, but repeat migrations cause duplicates

        self.stdout.write("Completed")
