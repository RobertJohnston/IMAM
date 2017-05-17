import pandas as pd
import numpy as np

from temba_client.v2 import TembaClient
from datetime import date, datetime
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from isoweek import Week
from django.conf import settings
from django.core import management

from home.models import Program

class Command(BaseCommand):
    help = 'Imports program data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        management.call_command('import_contacts')
        management.call_command('import_program')
        management.call_command('import_stock')
        # management.call_command('import_warehouse')

        client = TembaClient('rapidpro.io', open('token').read().strip())

        # Import Program Data
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
        df = pd.read_sql_query("select * from program;", con=engine)


        df['year_weeknum'] = zip(df['year'], df['weeknum'])
        df['iso_year_weeknum'] = df['year_weeknum'].map(lambda x: Week(x[0], x[1]))

        year, week, _ = date.today().isocalendar()
        current_week = Week(year, week)

        # since how many week this report is about
        df['since_x_weeks'] = df['iso_year_weeknum'].map(lambda x: current_week - x)

        # .query('siteid>101110001')\
        # Calculate missing reports
        promiss = df.query('since_x_weeks>0')\
                .query('since_x_weeks<=8')\
                .groupby(['siteid', 'type'])['weeknum']\
                .unique()\
                .map(lambda x: list(sorted(set(range(week - 8, week)) - set(x))))\
                .to_frame()

        promiss = promiss.reset_index()
        promiss = promiss.rename(index=str, columns={"weeknum": "missing_program"})

        promiss['missing_program_len'] = promiss.missing_program.map(lambda x: (len(x)))

        # Create missing stock reports
        stock = pd.read_sql_query("select * from stock;", con=engine)
        stock['year_weeknum'] = zip(stock['year'], stock['weeknum'])
        stock['iso_year_weeknum'] = stock['year_weeknum'].map(lambda x: Week(x[0], x[1]))

        # since how many week this report is about
        stock['since_x_weeks'] = stock['iso_year_weeknum'].map(lambda x: current_week - x)

        # stock missing reports
        stomiss = stock.query('since_x_weeks>0')\
                       .query('since_x_weeks<=8')\
                       .query('siteid>101110001')\
                       .groupby(['siteid', 'type'])['weeknum']\
                       .unique()\
                       .map(lambda x: list(sorted(set(range(week - 8, week)) - set(x))))\
                       .to_frame()

        stomiss = stomiss.reset_index()
        stomiss = stomiss.rename(index=str, columns={"weeknum": "missing_stock"})
        stomiss['missing_stock_len'] = stomiss.missing_stock.map(lambda x: (len(x)))

        # Merge program and stock together
        missing_reports = pd.merge(promiss, stomiss, left_on=['siteid', 'type'], right_on=['siteid', 'type'],
                                   how='outer', sort=False)

        # Remove rows for complete reporting
        missing_reports = missing_reports.query('missing_program_len > 0 | missing_stock_len > 0')

        # Merge with all contacts
        contacts = pd.read_sql_query("select * from registration;", con=engine)
        reminders = pd.merge(missing_reports, contacts, on=['siteid', 'type'])
        reminders.sort()

        sites = pd.read_sql_query("select * from site;", con=engine)

        reminders_sites = pd.merge(reminders, sites, on=['siteid'])

        # Create reminders message
        reminders_sites['message'] = ""

        def create_message(row_in_df):
            row_in_df.message = "Dear %s from %s. Reminder to send" % (row_in_df['name'].rstrip('.'), row_in_df.sitename)
            if row_in_df.missing_program_len > 0:
                row_in_df.message += ' PROGRAM reports for weeks %s' % (", ".join(map(lambda x: str(x), row_in_df.missing_program)))

            if row_in_df.missing_program_len > 0 and row_in_df.missing_stock_len > 0:
                row_in_df.message += ' and STOCK reports for weeks %s.' % (", ".join(map(lambda x: str(x), row_in_df.missing_stock)))
            elif (np.isnan(row_in_df.missing_program_len) or not row_in_df.missing_program_len) and row_in_df.missing_stock_len > 0:
                row_in_df.message += ' STOCK reports for weeks %s.' % (", ".join(map(lambda x: str(x), row_in_df.missing_stock)))

            return row_in_df

        reminders_sites = reminders_sites.apply(create_message, axis=1)

        # Add the context of missing stock data for Warehouses.

        filename = "Weekly Reminders.xlsx"
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        reminders_sites.to_excel(writer, 'Sheet1')
        writer.save()
        writer.close()

        def send_reminders(row_in_df):
            print "Sending message '%s' to '%s' (%s)" % (row_in_df['message'], row_in_df['name'], row_in_df['contact_uuid'])
            # client.create_broadcast(row_in_df['message'], contacts=[row_in_df['contact_uuid']])

        reminders_sites.apply(send_reminders, axis=1)

        print("weekly reminders exported to Excel")