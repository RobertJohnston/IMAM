from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings
from load_data import rename_cols

# load_data_siteid

# to run python manage.py load_data

# remember to delete the table in PostGresSql before running load or the column names do not appear
# to address this issue, could insert a drop table command in this file below.

class Command(BaseCommand):
    help = 'Loads siteid data to SQL for IMAM website'

    # A command must define handle
    def handle(self, *args, **options):

        # Drop table if exists.
        # engine.execute(""" DROP TABLE IF EXISTS "%s" """ % (tablename))

        # Load Site ID dataframe
        df = pd.ExcelFile('/home/robert/Downloads/all_siteid.xls').parse('Sheet1')

        # Rename all the columns in the imported data

        # Change the order (the index) of the columns

        # set primary key
        df.set_index('siteid')

        # engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))

        try:
            df.to_sql('siteids', engine, schema='public', if_exists='replace')
            # when using if_exists='replace' then all column names are deleted
            # when using  if_exists='append' then all column names are maintained, but repeat migrations cause duplicates
            with engine.connect() as con:
                con.execute('ALTER TABLE siteids ADD PRIMARY KEY (siteid);')
                print("Site ID data added.")

        # KeyboardInterrupt - will likely never return an exception
        except KeyboardInterrupt:
            print("Interrupted...")

        self.stdout.write("Completed")
