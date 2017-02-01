from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings

from load_data import assign_state_lga_num

# Site IDs for the health care facilities for 12 northern Nigerian states

# to run python manage.py load_data

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Drop table if exists already
        # engine.execute(""" DROP TABLE IF EXISTS "%s """ % (tablename))

        # Load SITE ID dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('/home/robert/Downloads/all_siteid.xls').parse('Sheet1')

        assign_state_lga_num(df)

        columnsTitles = ['siteid', 'state', 'state_num', 'lga', 'lga_num', 'ward', 'sitename', 'x_lat', 'y_lat', 'notes']
        df = df.reindex(columns=columnsTitles)

        #set primary key
        df.set_index('siteid')

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df.to_sql('siteids', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE siteids ADD PRIMARY KEY (siteid);')
                print("SiteID data added.")

        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")

