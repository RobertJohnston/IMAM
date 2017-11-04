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
from home.utilities import exception_to_sentry


class Command(BaseCommand):
    help = 'Sends weekly reminders to personnel at sites through API'

    # sent failure note to sentry
    @exception_to_sentry
    # A command must define handle
    def handle(self, *args, **options):

        # first update database with most recent reports.
        management.call_command('import_all')

        client = TembaClient('rapidpro.io', open('token').read().strip())

        # Import Program Data
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
        df = pd.read_sql_query("select * from program;", con=engine)

        # try to find a way to replace sqlachemy with django engine

        df['year_weeknum'] = zip(df['year'].map(int), df['weeknum'].map(int))
        df['iso_year_weeknum'] = df['year_weeknum'].map(lambda x: Week(x[0], x[1]))

        year, week, _ = date.today().isocalendar()
        current_week = Week(year, week)

        # since how many week this report is about
        df['since_x_weeks'] = df['iso_year_weeknum'].map(lambda x: current_week - x)

        # TO TEST WITH ONLY ONE REPORT
        # Add line to promiss definition below
        # .query('siteid=201110009')\
        # remove this when done testing

        # Calculate missing reports
        promiss = df.query('since_x_weeks>0')\
                .query('since_x_weeks<=8') \
                .groupby(['siteid', 'type'])['weeknum']\
                .unique()\
                .map(lambda x: list(sorted(set(range(week - 8, week)) - set(x))))\
                .to_frame()

        promiss = promiss.reset_index()
        promiss = promiss.rename(index=str, columns={"weeknum": "missing_program"})

        promiss['missing_program_len'] = promiss.missing_program.map(lambda x: (len(x)))

        # Create missing stock reports
        stock = pd.read_sql_query("select * from stock;", con=engine)
        stock['year_weeknum'] = zip(stock['year'].map(int), stock['weeknum'].map(int))
        stock['iso_year_weeknum'] = stock['year_weeknum'].map(lambda x: Week(x[0], x[1]))

        # since how many week this report is about
        stock['since_x_weeks'] = stock['iso_year_weeknum'].map(lambda x: current_week - x)

        # TO TEST WITH ONLY ONE REPORT
        # Add line to stomiss definition below
        # .query('siteid=201110009')\
        # remove this when done testing

        # stock missing reports
        stomiss = stock.query('since_x_weeks>0')\
                       .query('since_x_weeks<=8') \
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
        # reminders.sort()

        sites = pd.read_sql_query("select * from site;", con=engine)

        reminders_sites = pd.merge(reminders, sites, on=['siteid'])

        # pandas has a bug and doesn't convert datetime that has timezone
        # to some internal format when we do the apply below
        reminders_sites['first_seen'] = reminders_sites['first_seen'].map(lambda x: x.replace(tzinfo=None))
        reminders_sites['last_seen'] = reminders_sites['last_seen'].map(lambda x: x.replace(tzinfo=None))

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

        # Create missing stock reports
        warehouse = pd.read_sql_query("select * from warehouse;", con=engine)

        # Introducing Year for analysis
        # must loop over the data in the pandas series to assign the new variable with isocalendar
        # warehouse['year'] = warehouse.last_seen.isocalendar()[0]

        # we are doing this during importation already
        # warehouse['year'] = warehouse['last_seen'].map(lambda x: x.isocalendar()[0])
        # print(warehouse['year'].value_counts())

        # FIXME - add cleaning to importation
        # Weeknum data are not clean - not int
        warehouse.weeknum = pd.to_numeric(warehouse.weeknum, errors='coerce')

        # Clean out of range identification data - this deletes entire row where a NaN is found
        # week 52 should not be hard coded.
        warehouse = warehouse.query('weeknum==weeknum').query('weeknum>=1').query('weeknum<=52')
        # Convert from float to int
        warehouse.weeknum = warehouse.weeknum.astype(int)

        warehouse['year_weeknum'] = zip(warehouse['year'], warehouse['weeknum'])
        warehouse['iso_year_weeknum'] = warehouse['year_weeknum'].map(lambda x: Week(x[0], x[1]))

        year, week, _ = date.today().isocalendar()
        current_week = Week(year, week)

        # since how many week this report is about
        warehouse['since_x_weeks'] = warehouse['iso_year_weeknum'].map(lambda x: current_week - x)

        # There are no types per se in warehouse data.  All sites are warehouses.
        # to make the code more generic, assign correction to type variable in import_warehouse
        # then all warehouses sites will be coded as 'sup'.

        # For variable below - will not show output if referred to as warehouse.type only as warehouse['type']
        warehouse['type'] = "Sup"
        # warehouse['type'].value_counts()

        # Merge siteID with first and second that all inactive sites are included in the analysis

        warehouse_stomiss = warehouse.query('since_x_weeks>0')\
                                     .query('since_x_weeks<=8')\
                                     .query('siteid<101110001')\
                                     .groupby(['siteid', 'type'])['weeknum']\
                                     .unique().map(lambda x: list(sorted(set(range(week - 8, week)) - set(x))))\
                                     .to_frame()

        warehouse_stomiss = warehouse_stomiss.reset_index()
        warehouse_stomiss = warehouse_stomiss.rename(index=str, columns={"weeknum": "missing_stock"})

        # Need to add first and second admin
        first = pd.read_sql_query("select * from First_admin;", con=engine)
        first['siteid'] = first.state_num
        first['sitename'] = first.state

        second = pd.read_sql_query("select * from second_admin;", con=engine)
        second['siteid'] = second.lga_num
        second['sitename'] = second.lga

        supervision_sites = pd.concat([second, first])

        supervision_stomiss = pd.merge(supervision_sites, warehouse_stomiss, on='siteid', how='outer')

        target_weeks = []
        for i in range(1, 9):
            target_weeks.append((current_week - i).week)

        target_weeks = list(reversed(target_weeks))

        supervision_stomiss['missing_stock'] = supervision_stomiss['missing_stock'].map(
            lambda x: x if x == x else target_weeks)

        supervision_stomiss['missing_stock_len'] = supervision_stomiss.missing_stock.map(lambda x: (len(x)))
        supervision_stomiss = supervision_stomiss.query('missing_stock_len > 0')

        # merge with contacts
        contacts = pd.read_sql_query("select * from registration;", con=engine)

        # FIXME ensure that we include all LGAs and State warehouses even if they are inactive

        # If using same code as implementation - then add type
        warehouse_reminders = pd.merge(supervision_stomiss, contacts, on=['siteid'])

        # pandas as some bug and doesn't managed to convert datetime that has timezone
        # to some internal format when we do the apply bellow
        warehouse_reminders['first_seen'] =  warehouse_reminders['first_seen'].map(lambda x: x.replace(tzinfo=None))
        warehouse_reminders['last_seen'] =  warehouse_reminders['last_seen'].map(lambda x: x.replace(tzinfo=None))

        warehouse_reminders['message'] = ""

        def create_message(row_in_df):
            row_in_df.message = "Dear %s from %s. Reminder to send" % (row_in_df['name'].rstrip('.'), row_in_df.sitename)
            row_in_df.message += ' STOCK reports for weeks %s.' % (", ".join(map(lambda x: str(x), row_in_df.missing_stock)))
            return row_in_df

        warehouse_reminders = warehouse_reminders.apply(create_message, axis=1)

        # FIXME merge reminders_sites and warehouse_reminders
        # for export in excel just in case we need to use old back system of sending reminders through import contacts
        filename = "Weekly Reminders.xlsx"
        writer = pd.ExcelWriter(filename, engine='xlsxwriter', options={'remove_timezone': True})
        reminders_sites.to_excel(writer, 'Sheet1')
        writer.save()
        writer.close()

        def send_reminders(row_in_df):
            print "[%s/%s %s] Sending message '%s' to '%s' (%s)" % (
                loop_informations["remaining"],
                loop_informations["total_number"],
                loop_informations["current"],
                row_in_df['message'].encode('UTF-8'),
                row_in_df['name'].encode('UTF-8'),
                row_in_df['contact_uuid'].encode('UTF-8')
            )
            # API CALL - send_reminders
            # Comment / Uncomment to run the API
            client.create_broadcast(row_in_df['message'], contacts=[row_in_df['contact_uuid']])
            loop_informations["remaining"] -= 1

        reminders_timer = datetime.now()

        loop_informations = {
            "remaining": len(reminders_sites),
            "current": "sites",
            "total_number": len(reminders_sites),
        }

        # Send reminders to API for implementation sites
        reminders_sites.apply(send_reminders, axis=1)


        loop_informations["remaining"] = len(warehouse_reminders)
        loop_informations["total_number"] = len(warehouse_reminders)
        loop_informations["current"] = "warehouse"

        # Send reminders to API for warehouses
        warehouse_reminders.apply(send_reminders, axis=1)

        print datetime.now().strftime('Weekly reminders sent at %d %b %Y %-H:%M:%S'), 'Took %s time to talk to the API' % (datetime.now() - reminders_timer)