from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load PROGRAM dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/pro.xlsx').parse('Runs')

        # to speed up testing take only first 30 lines
        df = df[0:30]

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


def rename_cols(dataframe):
    # edit the data in pandas

    # Registration database
    dataframe.rename(columns={'Contact UUID': 'contact_uuid'}, inplace=True)
    dataframe.rename(columns={'URN': 'urn'}, inplace=True)
    dataframe.rename(columns={'Name': 'name'}, inplace=True)
    dataframe.rename(columns={'Groups': 'groups'}, inplace=True)
    dataframe.rename(columns={'SiteID': 'siteid'}, inplace=True)
    dataframe.rename(columns={'Type': 'type'}, inplace=True)
    # Need to edit these date time variables to include Time Zone for Postgresql
    dataframe.rename(columns={'First Seen': 'first_seen'}, inplace=True)
    dataframe.rename(columns={'Last Seen': 'last_seen'}, inplace=True)
    # change variable name of the following
    dataframe.rename(columns={'Mail (Value) - IMAM Register': 'mail'}, inplace=True)
    dataframe.rename(columns={'Post_imp (Value) - IMAM Register': 'post'}, inplace=True)

    # Program database
    dataframe.rename(columns={'WeekNum (Value) - IMAM Program': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'Role (Value) - IMAM Program': 'role'}, inplace=True)
    dataframe.rename(columns={'Type (Value) - IMAM Program': 'type'}, inplace=True)
    dataframe.rename(columns={'ProSiteID (Value) - IMAM Program': 'prositeid'}, inplace=True)
    dataframe.rename(columns={'ProType (Value) - IMAM Program': 'protype'}, inplace=True)
    dataframe.rename(columns={'age group (Value) - IMAM Program': 'age_group'}, inplace=True)
    # Outpatients admissions and exits
    dataframe.rename(columns={'Beg_o (Value) - IMAM Program': 'beg'}, inplace=True)
    dataframe.rename(columns={'Amar_o (Value) - IMAM Program': 'amar'}, inplace=True)
    dataframe.rename(columns={'Tin_o (Value) - IMAM Program': 'tin'}, inplace=True)
    dataframe.rename(columns={'Dcur_o (Value) - IMAM Program': 'dcur'}, inplace=True)
    dataframe.rename(columns={'Dead_o (Value) - IMAM Program': 'dead'}, inplace=True)
    dataframe.rename(columns={'DefU_o (Value) - IMAM Program': 'defu'}, inplace=True)
    dataframe.rename(columns={'Dmed_o (Value) - IMAM Program': 'dmed'}, inplace=True)
    dataframe.rename(columns={'Tout_o (Value) - IMAM Program': 'tout'}, inplace=True)
    # confirm correct data entry
    dataframe.rename(columns={'Confirm (Category) - IMAM Program': 'confirm'}, inplace=True)

    # Stock database

    # LGA database

    return dataframe


def merge_in_and_outpatients(dataframe):
    # convert admissions and exits to one column a piece not duplicates for out / in patients
    dataframe['beg'] = np.where(dataframe['type'] == "SC", dataframe['Beg_i (Value) - IMAM Program'], dataframe['beg'])
    dataframe['amar'] = np.where(dataframe['type'] == "SC", dataframe['Amar_i (Value) - IMAM Program'], dataframe['amar'])
    dataframe['tin'] = np.where(dataframe['type'] == "SC", dataframe['Tin_i (Value) - IMAM Program'], dataframe['tin'])
    dataframe['dcur'] = np.where(dataframe['type'] == "SC", dataframe['Dcur_i (Value) - IMAM Program'], dataframe['dcur'])
    dataframe['dead'] = np.where(dataframe['type'] == "SC", dataframe['Dead_i (Value) - IMAM Program'], dataframe['dead'])
    dataframe['defu'] = np.where(dataframe['type'] == "SC", dataframe['DefU_i (Value) - IMAM Program'], dataframe['defu'])
    dataframe['dmed'] = np.where(dataframe['type'] == "SC", dataframe['Dmed_i (Value) - IMAM Program'], dataframe['dmed'])
    dataframe['tout'] = np.where(dataframe['type'] == "SC", dataframe['Tout_i (Value) - IMAM Program'], dataframe['tout'])

    return dataframe