from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from isoweek import Week
from home.models import RawStock, Stock, LastUpdatedAPICall, Site

from home.utilities import exception_to_sentry
from home.utilities import clean

# import_stock.py
# to run python manage.py import_stock

# Change data entry to accept all data and clean data  after
# 1 -  to import data as JSON
# 2 -  import to Postgres as raw data
# 3 -  do data cleaning as save as clean data


class Command(BaseCommand):
    help = 'Import Stock data from RawStock'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Import all data',
        )

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):
        with transaction.atomic():

            last_update_time = LastUpdatedAPICall.objects.filter(kind="stock2").first()

            counter = RawStock.objects.all().count()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                Stock.objects.all().delete()
                data_to_process = RawStock.objects.all()

            elif options['all'] and not last_update_time:
                Stock.objects.all().delete()
                data_to_process = RawStock.objects.all()
                last_update_time = LastUpdatedAPICall(kind="stock2")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all datcountersince timestamp of last time
                # remember to use modified_on not last seen
                data_to_process = RawStock.objects.filter(modified_on__gte=last_update_time.timestamp)
                counter = RawStock.objects.filter(modified_on__gte=last_update_time.timestamp).count()

            elif not options['all'] and not last_update_time:
                Stock.objects.all().delete()
                data_to_process = RawStock.objects.all()
                last_update_time = LastUpdatedAPICall(kind="stock2")
            else:
                raise Exception()
                # This is unncessary in this context but good programming practice

            last_update_time.timestamp = datetime.now()

            # Create a cache - is this still used?
            # site_cache = {x.siteid: x for x in Site.objects.all()}

            for row in data_to_process.iterator():
                id = row.id
                counter-= 1

                # Update stock if id exists in Stock.objects
                if Stock.objects.filter(id=id):
                    stock_in_db = Stock.objects.get(id=id)
                # Create contact if id does not exist already
                else:
                    stock_in_db = Stock()
                    stock_in_db.id = id

                # If not confirmed, skip row data, do not add to database
                if row.confirm != "Yes":
                    print "             unconfirmed"
                    continue

                # SiteID
                if clean(row.siteid) is not None:
                    stock_in_db.siteid = clean(row.siteid)
                else:
                    print '             bad siteid: %s' % row.siteid
                    continue

                # If SiteID was training data entry or is invalid - skip entire row
                # No siteids exist between 3699 and 101110001
                # SiteIDs in Abia state - 101110001 to <200000000
                # SiteIDS in Zamfara state from 3901110001 to 3901110999
                if stock_in_db.siteid < 200000000 or stock_in_db.siteid > 3999999999:
                    print '             Incorrect siteid: %s' % stock_in_db.siteid
                    continue

                stock_in_db.contact_uuid = row.contact_uuid
                stock_in_db.urn    = row.urn
                stock_in_db.name   = row.name

                stock_in_db.first_seen = row.first_seen
                stock_in_db.last_seen = row.last_seen

                # Note, the in operator evaluates the details in the list of elements
                if row.type in ("OTP", "SC"):
                    stock_in_db.type = row.type
                else:
                    print '             bad type (OTP or SC) %s' % row.type
                    continue


                # Data cleaning for stock
                # OUTPATIENTS
                if  stock_in_db.type == "OTP" :
                    stock_in_db.rutf_in   = clean(row.rutf_in)
                    stock_in_db.rutf_out  = round(clean(row.rutf_used_carton) + clean(row.rutf_used_sachet) / 150., 2)
                    stock_in_db.rutf_bal  = round(clean(row.rutf_bal_carton) + clean(row.rutf_bal_sachet) / 150., 2)

                # INPATIENTS
                elif stock_in_db.type == "SC":

                    # F75 sachets per carton - 120
                    stock_in_db.f75_bal = round(clean(row.f75_bal_carton) + clean(row.f75_bal_sachet) / 120., 2)
                    # F100 sachets per carton - 90
                    stock_in_db.f100_bal = round(clean(row.f100_bal_carton) + clean(row.f100_bal_sachet) / 90., 2)
                    # print(' F75 BAL=%s F100 BAL=%s' % (stock_in_db.f75_bal, stock_in_db.f100_bal))

                # Entry of confirmed excessive reported stock of f75 and f100
                if stock_in_db.f75_bal > 9999:
                    print('     Excess number cartons for f75 %s, skip' % stock_in_db.f75_bal)
                    continue

                if stock_in_db.f100_bal > 9999:
                    print('    Excess number cartons for f75 %s, skip' % stock_in_db.f100_bal)
                    continue


                # Double counting
                # If cartons>1 and cartons *150  = sachets +/- 150 then cartons = sachets/150
                # RUTF_USED
                if clean(row.rutf_used_carton) is not None and clean(row.rutf_used_sachet) is not None:
                    if float(row.rutf_used_carton) > 1 and (-150 < (float(row.rutf_used_carton) * 150 - float(row.rutf_used_sachet)) < 150):
                        stock_in_db.rutf_out = round(float(row.rutf_used_sachet) / 150., 2)
                        # print("RUTF Used Carton=% RUTF Used Sachet=%  DOUBLE counting RUTF Used" % (row.rutf_used_carton, row.rutf_used_sachet))
                    # RUTF_BAL
                    if float(row.rutf_bal_carton) > 1 and (-150 < (float(row.rutf_bal_carton) * 150 - float(row.rutf_bal_sachet)) < 150):
                        stock_in_db.rutf_bal = round(float(row.rutf_bal_sachet) / 150., 2)
                        # print("RUTF Bal Carton=% RUTF Bal Sachet=%  DOUBLE counting RUTF Bal" % (row.rutf_bal_carton, row.rutf_bal_sachet))


                # Entry of decimal points
                # print(' RUTF IN=%s RUTF OUT=%s RUTF BAL=%s' % (stock_in_db.rutf_in, stock_in_db.rutf_out, stock_in_db.rutf_bal))

                # Entry of confirmed excessive numbers
                if stock_in_db.rutf_in > 9999:
                    print '    carton number for rutf_in is too big %s, skip' % stock_in_db.rutf_in
                    continue

                if stock_in_db.rutf_out > 9999:
                    print '    carton number for rutf_out is too big %s, skip' % stock_in_db.rutf_out
                    continue

                if stock_in_db.rutf_bal > 9999:
                    print '    carton number for rutf_bal is too big %s, skip' % stock_in_db.rutf_bal
                    continue


                # Create state_num and LGA_num
                # Implementation and LGA level
                if len(str(stock_in_db.siteid)) == 9 or len(str(stock_in_db.siteid)) == 3:
                    stock_in_db.state_num = int(str(stock_in_db.siteid)[:1])
                    stock_in_db.lga_num = int(str(stock_in_db.siteid)[:3])
                elif len(str(stock_in_db.siteid)) == 10 or len(str(stock_in_db.siteid)) == 4:
                    stock_in_db.state_num = int(str(stock_in_db.siteid)[:2])
                    stock_in_db.lga_num = int(str(stock_in_db.siteid)[:4])
                # State level
                elif len(str(stock_in_db.siteid)) == 1 or len(str(stock_in_db.siteid)) == 2:
                    stock_in_db.state_num = int(stock_in_db.siteid)
                    stock_in_db.lga_num = None
                else:
                    print(stock_in_db.siteid)
                    raise Exception()

                stock_in_db.weeknum = clean(row.weeknum)

                # Double check
                # Change 53 to max week number for year
                if stock_in_db.weeknum < 1 or stock_in_db.weeknum > 53:
                    print('     WEEKNUM < 1 or > 53 (%s), skip' % (stock_in_db.weeknum))
                    continue

                if stock_in_db.state_num >= 37:
                    print('     STATE id error (%s), skip' % (stock_in_db.state_num))
                    continue

                if 101 >= stock_in_db.lga_num or stock_in_db.lga_num >= 3799:
                    print('     LGA id error (%s), skip' % (stock_in_db.lga_num))
                    continue

                if 0 >= stock_in_db.siteid or stock_in_db.siteid >= 3799990999:
                    print('     SITEID error (%s), skip' % (stock_in_db.siteid))
                    continue


                # Introducing Year for X axis
                stock_in_db.year = stock_in_db.last_seen.isocalendar()[0]
                last_seen_weeknum = stock_in_db.last_seen.isocalendar()[1]

                # If report was for weeknum in last year but report data is this year, subtract one year from dataframe.year.
                # this double conditional identifies the year correctly in the majority of cases
                # except for reports with weeknum <=44 and more than 8 weeks in past
                if stock_in_db.weeknum > 44 and last_seen_weeknum < stock_in_db.weeknum:
                    stock_in_db.year -= 1

                today_year = date.today().year
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
                # Remove future reporting - stock data cannot surpass report WN and current year.
                if stock_in_db.year == today_year and stock_in_db.weeknum > rep_weeknum:
                    print('     Future reporting WEEKNUM (%s) current weeknum (%s)' % (
                    stock_in_db.weeknum, rep_weeknum))
                    continue

                # Delete all future reporting -before 12 PM on the first day of the report week.
                # This could be zero on Ramadan or holiday
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


                # Report is X weeks before current week number
                # stock_in_db.since_x_weeks = current_week - iso_year_weeknum


                # Variables to accelerate analysis

                # if we don't have the site in the database, skip entry
                if not Site.objects.filter(siteid=stock_in_db.siteid).exists():
                    continue

                print("Stock count %s" % counter)
                stock_in_db.save()

                site = Site.objects.get(siteid=stock_in_db.siteid)

                # Latest stock reports for OTP and SC
                if stock_in_db.type == "OTP":
                    # if site.otp is Null or False
                    if not site.otp:
                        # set site.otp to True
                        site.otp = True
                        site.save()

                    if site.latest_stock_report_otp is None or\
                                    (site.latest_stock_report_otp.year, site.latest_stock_report_otp.weeknum)\
                                        < (stock_in_db.year, stock_in_db.weeknum):
                        site.latest_stock_report_otp = stock_in_db
                        site.save()

                if stock_in_db.type == "SC":
                    if not site.sc:
                        site.sc = True
                        site.save()

                    if site.latest_stock_report_sc is None or\
                                    (site.latest_stock_report_sc.year, site.latest_stock_report_sc.weeknum)\
                                        < (stock_in_db.year, stock_in_db.weeknum):
                        site.latest_stock_report_sc = stock_in_db
                        site.save()

                # Drop duplicates
                # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                for oldest_stock_report in Stock.objects.filter(
                        siteid=stock_in_db.siteid,
                        year=stock_in_db.year,
                        weeknum=stock_in_db.weeknum,
                        type=stock_in_db.type).order_by('-last_seen')[1:]:
                    print("     Drop Duplicate")
                    oldest_stock_report.delete()

            last_update_time.save()





