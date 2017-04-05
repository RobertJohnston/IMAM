from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings

from load_data import rename_cols, \
                    merge_in_and_outpatients, \
                    add_program_reports_from_supervision, \
                    generic_cleaning, \
                    add_iso_dates, \
                    drop_duplicate_reports, \
                    program_cleaning

# PROGRAM DATA

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Load PROGRAM dataframe - for PROGRAM- use 'Runs' tab and not 'Contacts'
        df_raw = pd.ExcelFile('/home/robert/Downloads/pro.xlsx').parse('Runs')

        # Primary key for program data
        # Multi-index
        #   'urn'
        #   'first_seen'

        # to speed up testing take only first 30 lines
        # df_raw = df_raw[0:30]

        # Rename all the columns in the imported data
        rename_cols(df_raw)

        # Merge separate inpatients and outpatients variable into one variable / column
        merge_in_and_outpatients(df_raw)

        add_program_reports_from_supervision(df_raw)

        # Drop all unneccesary program variables
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
                         'age_group',
                         'beg',
                         'amar',
                         'tin',
                         'dcur',
                         'dead',
                         'defu',
                         'dmed',
                         'tout',
                         'confirm']
        df = df_raw.reindex(columns=columnsTitles)
        # Cannot make code above work in a function without the change of name of the df



        # Data cleaning and preparation
        generic_cleaning(df)
        add_iso_dates(df)
        drop_duplicate_reports(df)

        # Program specific data cleaning
        program_cleaning(df)


        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            # df.to_sql('pro_raw', engine, schema='public', if_exists='replace')
            # with engine.connect() as con:
            #     con.execute('ALTER TABLE program ADD PRIMARY KEY (urn, first_seen);')
            #     # add time zones with same code
            #     print("pro_raw data added.")

            df.to_sql('program', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE program ADD PRIMARY KEY (urn, first_seen);')
                # is primary key necessary ?
                print("program data added.")

        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")

