from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from temba_client.v2 import TembaClient
from isoweek import Week
from home.models import Stock, Registration, LastUpdatedAPICall, Site

from uuid import UUID

# import_stock.py
# to run python manage.py import_stock
# imports data from RapidPro API, cleans data and saves to Postgres

class Command(BaseCommand):
    help = 'Imports stock data to SQL through API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Import all data',
        )
        
    # A command must define handle
    def handle(self, *args, **options):
        client = TembaClient('rapidpro.io', open('token').read().strip())

        contact_cache = {x.contact_uuid: x for x in Registration.objects.all()}

        last_update_time = LastUpdatedAPICall.objects.filter(kind="stock").first()

        # Code below is explicitly describing all possible four conditions.
        # T/T   T/F    F/T    F/F
        if options['all'] and last_update_time:
            clients_from_api = client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d')

        elif options['all'] and not last_update_time:
            clients_from_api = client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d')
            last_update_time = LastUpdatedAPICall(kind="stock")

        elif not options['all'] and last_update_time:
            clients_from_api = client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d', after=last_update_time.timestamp)

        elif not options['all'] and not last_update_time:
            clients_from_api = client.get_runs(flow=u'a678268d-0e42-43f1-82cd-aa12117d145d')
            last_update_time = LastUpdatedAPICall(kind="stock")

        last_update_time.timestamp = datetime.now()

        site_cache = {x.siteid: x for x in Site.objects.all()}

        a = 0
        # rapidpro expects a uuid to identify flow instead of a flow name
        # https://app.rapidpro.io/flow/editor/a678268d-0e42-43f1-82cd-aa12117d145d/
        for stock_batch in clients_from_api.iterfetches(retry_on_rate_exceed=True):

            with transaction.atomic():
            # Optimization tool - transaction.atomic -is turned off here as it hides errors.

                # the API response is a list in a list
                # to interpret this you have to loop over the content
                for stock in stock_batch:
                    if 'confirm' not in stock.values or stock.values['confirm'].category != 'Yes':
                        print('     Unconfirmed Entry')
                        continue

                    if 'weeknum' not in stock.values:
                        print('     Entry without a weeknum, skip it')
                        continue

                    # if id of stock exists then update the row
                    if Stock.objects.filter(id=stock.id).exists():
                        stock_in_db = Stock.objects.get(id=stock.id)

                    # if id of stock data doesn't exist then create a new row.
                    else:
                        stock_in_db = Stock()
                        stock_in_db.id = stock.id

                    contact = contact_cache[stock.contact.uuid]
                    stock_in_db.contact_uuid = stock.contact.uuid
                    stock_in_db.urn = contact.urn
                    stock_in_db.name = contact.name

                    stock_in_db.siteid = contact.siteid

                    stock_in_db.weeknum = stock.values['weeknum'].value

                    stock_in_db.first_seen = stock.created_on
                    stock_in_db.last_seen =  stock.modified_on

                    # implementation
                    if 'route_by_type' in stock.values:
                        stock_in_db.type = stock.values['route_by_type'].category
                    # supervision
                    elif 'route_by_level' in stock.values:
                        stock_in_db.type = stock.values['stotype'].category
                        stock_in_db.siteid = stock.values['stositeid'].value
                    else:
                        raise Exception()

                    # FIXME probable error here with rutf_bal versus rutf_bal_carton & rutf_bal_sachet
                    if stock_in_db.type == 'OTP':
                        stock_in_db.rutf_in = stock.values['rutf_in'].value if stock.values['rutf_in'].value < 9999 else None
                        stock_in_db.rutf_used_carton = stock.values['rutf_used_carton'].value if stock.values['rutf_used_carton'].value < 9999 else None
                        stock_in_db.rutf_used_sachet = stock.values['rutf_used_sachet'].value if stock.values['rutf_used_sachet'].value < 9999 else None
                        stock_in_db.rutf_bal_carton = stock.values['rutf_bal_carton'].value   if stock.values['rutf_bal_carton'].value < 9999 else None
                        stock_in_db.rutf_bal_sachet = stock.values['rutf_bal_sachet'].value   if stock.values['rutf_bal_sachet'].value < 9999 else None

                        stock_in_db.rutf_out = stock_in_db.rutf_used_carton + (stock_in_db.rutf_used_sachet/150)
                        stock_in_db.rutf_bal = stock_in_db.rutf_bal_carton + (stock_in_db.rutf_bal_sachet/150)

                    elif stock_in_db.type == 'SC':
                        # for stabilization center only balance
                        stock_in_db.f100_bal_carton = stock.values['f100_bal_carton'].value if stock.values['f100_bal_carton'].value < 9999 else None
                        stock_in_db.f100_bal_sachet = stock.values['f100_bal_sachet'].value if stock.values['f100_bal_sachet'].value < 9999 else None
                        stock_in_db.f75_bal_carton = stock.values['f75_bal_carton'].value   if stock.values['f75_bal_carton'].value < 9999 else None
                        stock_in_db.f75_bal_sachet = stock.values['f75_bal_sachet'].value   if stock.values['f75_bal_sachet'].value < 9999 else None
                    else:
                        raise Exception()


                    # Introducing Year for X axis
                    # Remember that this code is running in a loop over all rows in data during the api call
                    stock_in_db.year = stock_in_db.last_seen.isocalendar()[0]
                    last_seen_weeknum = stock_in_db.last_seen.isocalendar()[1]

                    # If report was for weeknum in last year but report data is this year, subtract one year from dataframe.year.
                    # this double conditional identifies the year correctly in the majority of cases
                    # except for reports with weeknum <=44 and more than 8 weeks in past
                    if stock_in_db.weeknum > 44 and last_seen_weeknum < stock_in_db.weeknum:
                        stock_in_db.year -= 1

                    # FIXME
                    # add data cleaning

                    # df = df.query('not (weeknum < 22 & year <=2016)')
                    # df = df.query('not (weeknum > %s & year ==%s)' % (week, year))
                    # df = df.query('year >= 2016')
                    # remove future reports


                    today_year = date.today().year
                    today_weeknum = date.today().isocalendar()[1]
                    rep_weeknum = stock_in_db.last_seen.isocalendar()[1]

                    # Stock reporting with RapidPro started in June 2016 (week 22)
                    if stock_in_db.year == 2016 and stock_in_db.weeknum < 22:
                        print('     Training data - (%s %s)' % (stock_in_db.year, stock_in_db.weeknum))
                        continue

                    # Remove any cases from 2015

                    # Remove future reporting - recent data cannot surpass current year.
                    if stock_in_db.year > today_year:
                        print('     Future reporting YEAR (%s)' % (stock_in_db.year))
                        continue
                    # Remove future reporting - program data cannot surpass report WN and current year.
                    if stock_in_db.year == today_year and stock_in_db.weeknum > rep_weeknum :
                        print('     Future reporting WEEKNUM (%s) current weeknum (%s)' % (stock_in_db.weeknum, rep_weeknum))
                        continue

                    # Delete all future reporting - before 12 PM on the first day of the report week.
                    last_seen_dotw = stock_in_db.last_seen.isocalendar()[2]
                    last_seen_hour = stock_in_db.last_seen.hour

                    if last_seen_dotw == 1 and last_seen_hour < 12 and rep_weeknum == stock_in_db.weeknum:
                        print('     Monday AM reporting (%s)' % (stock_in_db.last_seen.strftime("%d-%m-%Y %H:%M:%S")))
                        continue

                    rep_year_wn = stock_in_db.last_seen.isocalendar()
                    iso_rep_year_wn = Week(int(rep_year_wn[0]), int(rep_year_wn[1]))
                    iso_year_weeknum = Week(int(stock_in_db.year), int(stock_in_db.weeknum))

                    stock_in_db.iso_diff = (iso_year_weeknum - iso_rep_year_wn)

                    # remove reports for 8 weeks prior to report date
                    if stock_in_db.iso_diff < -8:
                        print('     ISO DIFF: %s, last_seen: %s, last_seen_weeknum: %s, weeknum: %s, year: %s)' % (
                            stock_in_db.iso_diff, stock_in_db.last_seen.strftime("%d-%m-%Y"),
                            last_seen_weeknum, int(stock_in_db.weeknum), stock_in_db.year,
                        ))
                        continue


                    # Create state_num and LGA_num
                    # Implementation and LGA level
                    if len(str(contact.siteid)) == 9 or len(str(contact.siteid)) == 3:
                        stock_in_db.state_num = int(str(contact.siteid)[:1])
                        stock_in_db.lga_num = int(str(contact.siteid)[:3])
                    elif len(str(contact.siteid)) == 10 or len(str(contact.siteid)) == 4:
                        stock_in_db.state_num = int(str(contact.siteid)[:2])
                        stock_in_db.lga_num = int(str(contact.siteid)[:4])
                    # State level
                    elif len(str(contact.siteid)) == 1 or len(str(contact.siteid)) == 2:
                        stock_in_db.state_num = int(contact.siteid)
                        stock_in_db.lga_num = None
                    else:
                        raise Exception()

                    if stock_in_db.siteid not in site_cache:
                        continue

                    site = site_cache[stock_in_db.siteid]

                    stock_in_db.save()  # Drop duplicates

                    if stock_in_db.type == "OTP":
                        if not site.otp:
                            site.otp = True
                            site.save()

                        if site.latest_stock_report_otp is None or \
                                        (site.latest_stock_report_otp.year, site.latest_stock_report_otp.weeknum) \
                                        < (stock_in_db.year, stock_in_db.weeknum):
                            site.latest_stock_report_otp = stock_in_db
                            site.save()

                    if stock_in_db.type == "SC":
                        if not site.sc:
                            site.sc = True
                            site.save()

                        if site.latest_stock_report_sc is None or \
                                        (site.latest_stock_report_sc.year, site.latest_stock_report_sc.weeknum) \
                                        < (stock_in_db.year, stock_in_db.weeknum):
                            site.latest_stock_report_sc = stock_in_db
                            site.save()

                    # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                    for oldest_stock_report in Stock.objects.filter(
                        siteid=contact.siteid,
                        year=stock_in_db.year,
                        weeknum=stock_in_db.weeknum,
                        type=stock_in_db.type).order_by('-last_seen')[1:]:

                        print ("     Drop Duplicate")
                        oldest_stock_report.delete()
            
                    a += 1
                    print(a)

        last_update_time.save()