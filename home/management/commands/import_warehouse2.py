from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from isoweek import Week
from home.models import RawWarehouse, Warehouse, Site, LastUpdatedAPICall


# This code is duplicated in from import_program2 and import_warehouse2
def clean(value_to_clean):
    try:
        return int(float(value_to_clean))
    except (ValueError, TypeError):
        print("Fail to convert '%s' as a number" % (value_to_clean))
        return None


# imports data from Raw Warehouse, cleans data and saves to Postgres

class Command(BaseCommand):
    help = 'Imports raw_warehouse data to clean and saves in PostGres'

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
        with transaction.atomic():

            last_update_time = LastUpdatedAPICall.objects.filter(kind="warehouse").first()

            counter= RawWarehouse.objects.all().count()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                Warehouse.objects.all().delete()
                data_to_process = RawWarehouse.objects.all()

            elif options['all'] and not last_update_time:
                Warehouse.objects.all().delete()
                data_to_process = RawWarehouse.objects.all()
                last_update_time = LastUpdatedAPICall(kind="warehouse")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                # remember to use modified_on not last seen
                data_to_process = RawWarehouse.objects.filter(modified_on__gte=last_update_time.timestamp)
                counter = RawWarehouse.objects.filter(modified_on__gte=last_update_time.timestamp).count()

            elif not options['all'] and not last_update_time:
                Warehouse.objects.all().delete()
                data_to_process = RawWarehouse.objects.all()
                last_update_time = LastUpdatedAPICall(kind="warehouse")
            else:
                raise Exception()
                # This is unncessary in this context but good programming practice

            last_update_time.timestamp = datetime.now()

            site_cache = {x.siteid: x for x in Site.objects.all()}

            for row in data_to_process.iterator():
                id = row.id
                counter -= 1

                # Update stock if id exists in Warehouse.objects
                if Warehouse.objects.filter(id=id):
                    warehouse_in_db = Warehouse.objects.get(id=id)
                # Create contact if id does not exist already
                else:
                    warehouse_in_db = Warehouse()
                    warehouse_in_db.id = id

                # If not confirmed, skip row data, do not add to database
                if row.confirm != "Yes":
                    print  "             Unconfirmed Entry"
                    continue

                # SiteID
                if clean(row.siteid) is not None:
                    warehouse_in_db.siteid = clean(row.siteid)
                else:
                    print '             bad siteid: %s' % row.siteid
                    continue

                # If SiteID was training data entry or is invalid - skip entire row
                # Supervision siteids range from 1 to 3699
                # No siteids exist between 3699 and 101110001
                # SiteIDs in Abia state - 101110001 to <200000000
                if warehouse_in_db.siteid > 3699:
                    print '             siteid is too big: %s' % warehouse_in_db.siteid
                    continue

                warehouse_in_db.contact_uuid = row.contact_uuid
                warehouse_in_db.urn = row.urn
                warehouse_in_db.name = row.name

                warehouse_in_db.first_seen = row.first_seen
                warehouse_in_db.last_seen = row.last_seen

                warehouse_in_db.rutf_in =  clean(row.rutf_in)
                warehouse_in_db.rutf_out = clean(row.rutf_out)
                warehouse_in_db.rutf_bal = clean(row.rutf_bal)

                warehouse_in_db.weeknum = clean(row.weeknum)

                if not warehouse_in_db.weeknum:
                    print('     Entry without a weeknum, skip it')
                    continue

                # Errors in Weeknum - Double check
                if warehouse_in_db.weeknum < 1 or warehouse_in_db.weeknum > 53:
                    print('     WEEKNUM < 1 or > 53 (%s), skip' % (warehouse_in_db.weeknum))
                    continue
                if warehouse_in_db.rutf_in > 999999:
                    print '    carton number for rutf_in is too big %s, skip' % warehouse_in_db.rutf_in
                    continue

                if warehouse_in_db.rutf_out > 999999:
                    print '    carton number for rutf_out is too big %s, skip' % warehouse_in_db.rutf_out
                    continue

                if warehouse_in_db.rutf_bal > 999999:
                    print '    carton number for rutf_bal is too big %s, skip' % warehouse_in_db.rutf_bal
                    continue


                warehouse_in_db.first_seen = row.first_seen
                warehouse_in_db.last_seen = row.last_seen


                # FIXME
                # Add data cleaning for implementation level who accidentally reported with the warehouse data entry

                # if siteid = one of list below then add to import normal stock data not warehouse data
                # better to identify all siteids > 3699
                # 3508110034
                # 3502110031
                # 3319110014 - error in registration - siteid does not exist
                # 3301110008
                # 827110013
                # 821110053



                # Introducing Year for X axis
                # Remember that this code is running in a loop over all data in the api call
                warehouse_in_db.year = warehouse_in_db.last_seen.isocalendar()[0]
                last_seen_weeknum = warehouse_in_db.last_seen.isocalendar()[1]

                # If report was for weeknum in last year but report data is this year, subtract one year from dataframe.year.
                # this double conditional identifies the year correctly in the majority of cases
                # except for reports with weeknum <=44 and more than 8 weeks in past
                if warehouse_in_db.weeknum > 44 and last_seen_weeknum < warehouse_in_db.weeknum:
                    warehouse_in_db.year -= 1


                today_year = date.today().year
                rep_weeknum = warehouse_in_db.last_seen.isocalendar()[1]

                # Stock reporting with RapidPro started in June 2016 (week 22)
                if warehouse_in_db.year == 2016 and warehouse_in_db.weeknum < 22:
                    print('     Training data - (%s %s)' % (warehouse_in_db.year, warehouse_in_db.weeknum))
                    continue

                # Remove any cases from 2015

                # Remove future reporting - recent data cannot surpass current year.
                if warehouse_in_db.year > today_year:
                    print('     Future reporting YEAR (%s)' % (warehouse_in_db.year))
                    continue
                # Remove future reporting - stock data cannot surpass report WN and current year.
                if warehouse_in_db.year == today_year and warehouse_in_db.weeknum > rep_weeknum:
                    print('     Future reporting WEEKNUM (%s) current weeknum (%s)' % (
                        warehouse_in_db.weeknum, rep_weeknum))
                    continue

                # Delete all future reporting -before 12 PM on the first day of the report week.
                # This could be zero on Ramadan or holiday
                last_seen_dotw = warehouse_in_db.last_seen.isocalendar()[2]
                last_seen_hour = warehouse_in_db.last_seen.hour

                if last_seen_dotw == 1 and last_seen_hour < 12 and rep_weeknum == warehouse_in_db.weeknum:
                    print('     Monday AM reporting (%s)' % (warehouse_in_db.last_seen.strftime("%d-%m-%Y %H:%M:%S")))
                    continue

                rep_year_wn = warehouse_in_db.last_seen.isocalendar()
                iso_rep_year_wn = Week(int(rep_year_wn[0]), int(rep_year_wn[1]))
                iso_year_weeknum = Week(int(warehouse_in_db.year), int(warehouse_in_db.weeknum))

                warehouse_in_db.iso_diff = (iso_year_weeknum - iso_rep_year_wn)

                # remove reports for 8 weeks prior to report date
                if warehouse_in_db.iso_diff < -8:
                    print('     ISO DIFF: %s, last_seen: %s, last_seen_weeknum: %s, weeknum: %s, year: %s)' % (
                        warehouse_in_db.iso_diff, warehouse_in_db.last_seen.strftime("%d-%m-%Y"),
                        last_seen_weeknum, int(warehouse_in_db.weeknum), warehouse_in_db.year,
                    ))
                    continue


                # Report is X weeks before current week number
                # warehouse_in_db.since_x_weeks = current_week - iso_year_weeknum


                print("count %s" % counter)
                warehouse_in_db.save()

                # Drop duplicates
                # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                for oldest_report in Warehouse.objects.filter(
                        siteid  = warehouse_in_db.siteid,
                        year    = warehouse_in_db.year,
                        weeknum = warehouse_in_db.weeknum).order_by('-last_seen')[1:]:
                    print("     Drop Duplicate")
                    oldest_report.delete()


        last_update_time.save()














