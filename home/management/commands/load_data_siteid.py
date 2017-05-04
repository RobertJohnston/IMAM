from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

from load_data import assign_state_lga_num

# Site IDs data for the health care facilities for 12 northern Nigerian states

# to run "python manage.py load_data_siteid"

class Command(BaseCommand):
    help = 'Loads sites data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Drop table if exists already

        # Load SITE ID dataframe
        # note for PROGRAM- use 'Runs' tab and not 'Contacts'
        df = pd.ExcelFile('all_siteid.xls').parse('Sheet1')

        assign_state_lga_num(df)

        # Opening date
        # Closing date

        # First Admin
        columnsTitles = ['state_num', 'state']
        first_admin_df = df.reindex(columns=columnsTitles)
        # drop all duplicates (keep first instance is default)
        first_admin_df = first_admin_df.drop_duplicates(['state_num'], keep='first')
        first_admin_df.state_num = first_admin_df.state_num.astype(int)
        first_admin_df = first_admin_df.sort_values(by='state_num')
        # in jupyter notebook - following line deletes 2nd index, here the 2nd old index is maintained.
        first_admin_df.reset_index(drop=True)

        # Second Admin
        columnsTitles = ['lga_num', 'lga', 'state_num']
        second_admin_df = df.reindex(columns=columnsTitles)
        second_admin_df = second_admin_df.drop_duplicates(['lga_num'], keep='first')
        # instead of filtering out only the LGA sites, just deleting cases of lga_num == NaN which are only found in
        # state level sites
        from ipdb import set_trace; set_trace()
        second_admin_df = second_admin_df.query('lga_num==lga_num')
        second_admin_df.lga_num = second_admin_df.lga_num.astype(int)
        second_admin_df = second_admin_df.sort_values(by='lga_num')
        second_admin_df.reset_index(drop=True)

        # Implementation Sites
        columnsTitles = ['siteid', 'sitename', 'state_num', 'lga_num', 'ward',  'x_long', 'y_lat', 'notes']
        site_df = df.reindex(columns=columnsTitles)

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            first_admin_df.to_sql('first_admin', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE first_admin ADD PRIMARY KEY (state_num);')
                print("First admin data added.")

            second_admin_df.to_sql('second_admin', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE second_admin ADD PRIMARY KEY (lga_num);')
                print("Second admin data added.")

            site_df.to_sql('site', engine, schema='public', if_exists='replace')
            with engine.connect() as con:
                con.execute('ALTER TABLE site ADD PRIMARY KEY (siteid);')
                print("Site data added.")

        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")

