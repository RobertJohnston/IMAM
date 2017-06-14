from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from isoweek import Week
from home.models import RawProgram, Program, LastUpdatedAPICall, Site


# import_program.py
# to run python manage.py import_program
# imports program data from RapidPro API, cleans data and saves to Postgres

# Change data entry to accept all data and clean data  after
# 1 -  to import data as JSON
# 2 -  import to Postgres as raw data
# 3 -  do data cleaning as save as clean data

# Currently Data errors such as strings instead of integers are not available
# Other data entry mistakes such as aberrant values are still visible.

class Command(BaseCommand):
    help = 'Import Program data from RawProgram'

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

            last_update_time = LastUpdatedAPICall.objects.filter(kind="program").first()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                Program.objects.all().delete()
                data_to_process = RawProgram.objects.all()

            elif options['all'] and not last_update_time:
                Program.objects.all().delete()
                data_to_process = RawProgram.objects.all()
                last_update_time = LastUpdatedAPICall(kind="program")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                # remember to use modified_on not last seen
                data_to_process = RawProgram.objects.filter(modified_on__gte=last_update_time.timestamp)

            elif not options['all'] and not last_update_time:
                Program.objects.all().delete()
                data_to_process = RawProgram.objects.all()
                last_update_time = LastUpdatedAPICall(kind="program")
            else:
                raise Exception()
                # This is unncessary in this context but good programming practice

            last_update_time.timestamp = datetime.now()

            site_cache = {x.siteid: x for x in Site.objects.all()}

            counter = RawProgram.objects.all().count()

            for program_row in data_to_process.iterator():
                id = program_row.id

                # countdown counter
                counter -= 1

                # Update program if id exists in Program.objects
                if Program.objects.filter(id=id):
                    program_in_db = Program.objects.get(id=id)
                # Create contact if id does not exist already
                else:
                    program_in_db = Program()
                    program_in_db.id = id

                # If confirmed, continue - if unconfirmed - skip entire row
                if program_row.confirm == "Yes":
                    program_in_db.confirm = program_row.confirm
                else:
                    continue

                # SiteID
                if program_row.siteid.isdigit():
                    program_in_db.siteid = int(program_row.siteid)
                else:
                    continue

                # If SiteID was training data entry or is invalid - skip entire row
                # No siteids exist between 3699 and 101110001
                # SiteIDs in Abia state - 101110001 to <200000000
                if program_in_db.siteid < 200000000:
                    continue

                program_in_db.contact_uuid = program_row.contact_uuid
                program_in_db.urn    = program_row.urn
                program_in_db.name   = program_row.name
                # program_in_db.role   = program_row.role

                program_in_db.first_seen = program_row.first_seen
                program_in_db.last_seen = program_row.last_seen

                # Note, the in operator evaluates the details in the list of elements
                if program_row.type in ("OTP", "SC"):
                    program_in_db.type = program_row.type
                else:
                    continue

                program_in_db.age_group = program_row.age_group

                def clean(value_to_clean):
                    try:
                        return int(float(value_to_clean))
                    except ValueError:
                        print("Fail to convert '%s' as a number" % (value_to_clean))
                        return None

                # Data cleaning for inpatients and outpatients
                program_in_db.weeknum = clean(program_row.weeknum)
                program_in_db.beg     = clean(program_row.beg)
                program_in_db.amar    = clean(program_row.amar)
                program_in_db.tin     = clean(program_row.tin) if program_row.tin is not None else 0
                program_in_db.dcur    = clean(program_row.dcur)
                program_in_db.dead    = clean(program_row.dead)
                program_in_db.defu    = clean(program_row.defu)
                program_in_db.dmed    = clean(program_row.dmed)
                program_in_db.tout    = clean(program_row.tout)

                # Create state_num and LGA_num
                # Implementation and LGA level
                if len(str(program_in_db.siteid)) == 9 or len(str(program_in_db.siteid)) == 3:
                    program_in_db.state_num = int(str(program_in_db.siteid)[:1])
                    program_in_db.lga_num = int(str(program_in_db.siteid)[:3])
                elif len(str(program_in_db.siteid)) == 10 or len(str(program_in_db.siteid)) == 4:
                    program_in_db.state_num = int(str(program_in_db.siteid)[:2])
                    program_in_db.lga_num = int(str(program_in_db.siteid)[:4])
                # State level
                elif len(str(program_in_db.siteid)) == 1 or len(str(program_in_db.siteid)) == 2:
                    program_in_db.state_num = int(program_in_db.siteid)
                    program_in_db.lga_num = None
                else:
                    print(program_in_db.siteid)
                    raise Exception()

                # Double check
                if program_in_db.weeknum < 1 or program_in_db.weeknum > 53:
                    print('     WEEKNUM < 1 or > 53 (%s), skip' % (program_in_db.weeknum))
                    continue

                if program_in_db.state_num >= 37:
                    print('     STATE id error (%s), skip' % (program_in_db.state_num))
                    continue

                if 101 >= program_in_db.lga_num or program_in_db.lga_num >= 3799:
                    print('     LGA id error (%s), skip' % (program_in_db.lga_num))
                    continue

                if 0 >= program_in_db.siteid or program_in_db.siteid >= 3799990999:
                    print('     SITEID error (%s), skip' % (program_in_db.siteid))
                    continue


                # Introducing Year for X axis
                program_in_db.year = program_in_db.last_seen.isocalendar()[0]
                last_seen_weeknum = program_in_db.last_seen.isocalendar()[1]

                # If report was for weeknum in last year but report data is this year, subtract one year from dataframe.year.
                # this double conditional identifies the year correctly in the majority of cases
                # except for reports with weeknum <=44 and more than 8 weeks in past
                if program_in_db.weeknum > 44 and last_seen_weeknum < program_in_db.weeknum:
                    program_in_db.year -= 1

                today_year = date.today().year
                today_weeknum = date.today().isocalendar()[1]
                rep_weeknum = program_in_db.last_seen.isocalendar()[1]

                # Program reporting with RapidPro started in June 2016 (week 22)
                if program_in_db.year == 2016 and program_in_db.weeknum < 22:
                    print('     Training data - (%s %s)' % (program_in_db.year, program_in_db.weeknum))
                    continue

                # Remove any cases from 2015

                # Remove future reporting - recent data cannot surpass current year.
                if program_in_db.year > today_year:
                    print('     Future reporting YEAR (%s)' % (program_in_db.year))
                    continue
                # Remove future reporting - program data cannot surpass report WN and current year.
                if program_in_db.year == today_year and program_in_db.weeknum > rep_weeknum:
                    print('     Future reporting WEEKNUM (%s) current weeknum (%s)' % (
                    program_in_db.weeknum, rep_weeknum))
                    continue

                # Delete all future reporting -before 12 PM on the first day of the report week.
                # This could be zero on Ramadan or holiday
                last_seen_dotw = program_in_db.last_seen.isocalendar()[2]
                last_seen_hour = program_in_db.last_seen.hour

                if last_seen_dotw == 1 and last_seen_hour < 12 and rep_weeknum == program_in_db.weeknum:
                    print('     Monday AM reporting (%s)' % (program_in_db.last_seen.strftime("%d-%m-%Y %H:%M:%S")))
                    continue

                rep_year_wn = program_in_db.last_seen.isocalendar()
                iso_rep_year_wn = Week(int(rep_year_wn[0]), int(rep_year_wn[1]))
                iso_year_weeknum = Week(int(program_in_db.year), int(program_in_db.weeknum))

                program_in_db.iso_diff = (iso_year_weeknum - iso_rep_year_wn)

                # remove reports for 8 weeks prior to report date
                if program_in_db.iso_diff < -8:
                    print('     ISO DIFF: %s, last_seen: %s, last_seen_weeknum: %s, weeknum: %s, year: %s)' % (
                        program_in_db.iso_diff, program_in_db.last_seen.strftime("%d-%m-%Y"),
                        last_seen_weeknum, int(program_in_db.weeknum), program_in_db.year,
                    ))
                    continue


                # Report is X weeks before current week number
                # program_in_db.since_x_weeks = current_week - iso_year_weeknum

                # Variables to accelerate analysis

                # if we don't have the site in the database, skip for now
                if program_in_db.siteid not in site_cache:
                    continue

                site = site_cache[program_in_db.siteid]

                print("count %s" % counter)
                program_in_db.save()

                if program_in_db.type == "OTP":
                    if not site.otp:
                        site.otp = True
                        site.save()

                    if site.latest_program_report_otp is None or\
                                    (site.latest_program_report_otp.year, site.latest_program_report_otp.weeknum)\
                                        < (program_in_db.year, program_in_db.weeknum):
                        site.latest_program_report_otp = program_in_db
                        site.save()

                if program_in_db.type == "SC":
                    if not site.sc:
                        site.sc = True
                        site.save()

                    if site.latest_program_report_sc is None or\
                                    (site.latest_program_report_sc.year, site.latest_program_report_sc.weeknum)\
                                        < (program_in_db.year, program_in_db.weeknum):
                        site.latest_program_report_sc = program_in_db
                        site.save()

                # Drop duplicates
                # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                for oldest_program_report in Program.objects.filter(
                        siteid=program_in_db.siteid,
                        year=program_in_db.year,
                        weeknum=program_in_db.weeknum,
                        type=program_in_db.type).order_by('-last_seen')[1:]:
                    print("     Drop Duplicate")
                    oldest_program_report.delete()



            last_update_time.save()





# IntegrityError: duplicate key value violates unique constraint "program_urn_30ba6b57_uniq"
# DETAIL:  Key (urn, first_seen)=(+2347061353772, 2017-06-01 08:53:19.799869+00) already exists.

