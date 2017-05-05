from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from temba_client.v2 import TembaClient
from isoweek import Week
from home.models import Program, Registration, LastUpdatedAPICall

from uuid import UUID

# import_program.py
# to run python manage.py import_program
# imports program data from RapidPro API, cleans data and saves to Postgres

# FIXME change data entry to accept all data
# create variable valid (true/false)
# Data errors such as strings instead of integers are not available
# Other data entry mistakes such as aberrant values are still visible.

class Command(BaseCommand):
    help = 'Imports program data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        client = TembaClient('rapidpro.io', open('token').read().strip())

        contact_cache = {x.contact_uuid: x for x in Registration.objects.all()}

        last_update_time = LastUpdatedAPICall.objects.filter(kind="program").first()

        if last_update_time:
            clients_from_api = client.get_runs(flow=u'a9eed2f3-a92c-48dd-aa10-4f139b1171a4', after=last_update_time.timestamp)
        else:
            clients_from_api = client.get_runs(flow=u'a9eed2f3-a92c-48dd-aa10-4f139b1171a4')
            last_update_time = LastUpdatedAPICall(kind="program")

        last_update_time.timestamp = datetime.now()

        a = 0
        # rapidpro expects a uuid to identify flow instead of a flow name
        # The uuid is in the url of the flow : for example https://app.rapidpro.io/flow/editor/a9eed2f3-a92c-48dd-aa10-4f139b1171a4/
        for program_batch in clients_from_api.iterfetches(retry_on_rate_exceed=True):

            with transaction.atomic():
            # Optimization tool - transaction.atomic -is turned off above as it hides errors.

                # the API response is a list in a list
                # to interpret this you have to loop over the content
                for program in program_batch:
                    if 'confirm' not in program.values or program.values['confirm'].category != 'Yes':
                        print('     Not CONFIRMED %s') % program.contact.name
                        continue

                    # if id of program exists then update the row
                    if Program.objects.filter(id=program.id).exists():
                        program_in_db = Program.objects.get(id=program.id)
                        print('Updating an existing program data')

                    # if id of program data doesn't exist then create a new row.
                    else:
                        program_in_db = Program()
                        program_in_db.id = program.id
                        print('Creating a new program data')

                    # if program.contact.uuid not in contact_cache:
                    #     print("      No Contact UUID in database %s" % program.contact.uuid)
                    #     # continue causes the import to skip this entry
                    #     # possible concurrency problem if someone registers during import_contacts and sends valid program data
                    #     continue

                    # Line below will cause import to crash if contact does not exist - one way to address concurrency problem.
                    contact = contact_cache[program.contact.uuid]
                    program_in_db.contact_uuid = program.contact.uuid
                    program_in_db.urn = contact.urn
                    program_in_db.name = contact.name

                    program_in_db.first_seen = program.created_on
                    program_in_db.last_seen = program.modified_on

                    # If report comes from supervisor, siteid (prosite) and site type (protype) is entered by supervisor
                    # and not taken directly from contacts data of reporter.
                    if 'prosite' in program.values:
                        program_in_db.siteid = program.values['prosite'].value
                    else:
                        program_in_db.siteid = contact.siteid

                    if 'type' in program.values:
                        site_type = program.values['type'].category.upper()
                    elif 'protype' in program.values:
                        site_type = program.values['protype'].category.upper()
                    else:
                        raise Exception()

                    program_in_db.weeknum = program.values['weeknum'].value
                    program_in_db.role = program.values['role'].value
                    # age_group = models.TextField(blank=True, null=True)

                    # in theory, if we take the category of variable type or protype, then only 2 answers should be OTP or SC
                    if site_type == "OTP":
                        program_in_db.beg =  program.values['beg_o'].value
                        program_in_db.amar = program.values['amar_o'].value

                        # program_in_db.tin = program.values['tin_o'].value
                        # one import from June 2016 where tin_o has KeyError
                        if 'tin_o' in program.values:
                            program_in_db.tin = program.values['tin_o'].value
                        else:
                            program_in_db.tin = 0
                            print("      tin_o KeyError - RapidPro error from %s" % program_in_db.last_seen)

                        program_in_db.dcur = program.values['dcur_o'].value
                        program_in_db.dead = program.values['dead_o'].value
                        program_in_db.defu = program.values['defu_o'].value
                        program_in_db.dmed = program.values['dmed_o'].value
                        program_in_db.tout = program.values['tout_o'].value

                    elif site_type == "SC":
                        program_in_db.beg =  program.values['beg_i'].value
                        program_in_db.amar = program.values['amar_i'].value
                        program_in_db.tin =  program.values['tin_i'].value
                        program_in_db.dcur = program.values['dcur_i'].value
                        program_in_db.dead = program.values['dead_i'].value
                        program_in_db.defu = program.values['defu_i'].value
                        program_in_db.dmed = program.values['dmed_i'].value
                        program_in_db.tout = program.values['tout_i'].value
                    else:
                        raise Exception()

                    program_in_db.type = site_type
                    program_in_db.confirm = program.values['confirm'].category

                    # Create state_num and LGA_num
                    # Implementation and LGA level
                    if len(str(contact.siteid)) == 9 or len(str(contact.siteid)) == 3:
                        program_in_db.state_num = int(str(contact.siteid)[:1])
                        program_in_db.lga_num = int(str(contact.siteid)[:3])
                    elif len(str(contact.siteid)) == 10 or len(str(contact.siteid)) == 4:
                        program_in_db.state_num = int(str(contact.siteid)[:2])
                        program_in_db.lga_num = int(str(contact.siteid)[:4])
                    # State level
                    elif len(str(contact.siteid)) == 1 or len(str(contact.siteid)) == 2:
                        program_in_db.state_num = int(contact.siteid)
                        program_in_db.lga_num = None
                    else:
                        raise Exception()


                    # FIXME filter siteid data
                    # What is needed here ?
                    # SiteID can be zero for national level registration

                    bad_data = False
                    for i in ('state_num', 'lga_num', 'siteid'):
                        if getattr(program_in_db, i) < 0:
                            bad_data = '        %s less than zero, skip' % i
                            break

                    if bad_data:
                        print (bad_data)
                        continue

                    # Double check
                    if program_in_db.weeknum < 1 or program_in_db.weeknum > 53:
                        print('     WEEKNUM < 1 or > 53 (%s), skip' % (program_in_db.weeknum))
                        continue

                    if program_in_db.state_num >= 37:
                        print('     STATE id error (%s), skip' % (program_in_db.state_num))
                        continue

                    if  101 >= program_in_db.lga_num or program_in_db.lga_num >= 3799:
                        print('     LGA id error (%s), skip' % (program_in_db.lga_num))
                        continue

                    if 0 >= program_in_db.siteid or program_in_db.siteid >= 3799990999:
                        print('     SITEID error (%s), skip' % (program_in_db.siteid))
                        continue

                    # # Introducing Year for X axis
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
                    # Remove future reporting - recent data cannot surpass current year.
                    if program_in_db.year > today_year:
                        print('     Future reporting YEAR (%s)' % (program_in_db.year))
                        continue
                    # Remove future reporting - program data cannot surpass report WN and current year.
                    if program_in_db.year == today_year and program_in_db.weeknum > rep_weeknum :
                        print('     Future reporting WEEKNUM (%s) current weeknum (%s)' % (program_in_db.weeknum, rep_weeknum))
                        continue

                    # Delete all future reporting -before 12 PM on the first day of the report week.
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

                    year, week, dotw = date.today().isocalendar()
                    current_week = Week(year, week)

                    # Report is X weeks before current week number
                    program_in_db.since_x_weeks = current_week - iso_year_weeknum

                    # TODO delete those columns
                    # last_seen_weeknum = models.BigIntegerField(blank=True, null=True)
                    # rep_year_wn = models.TextField(blank=True, null=True)
                    # rep_weeknum = models.BigIntegerField(blank=True, null=True)
                    # last_seen_dotw = models.BigIntegerField(blank=True, null=True)
                    # last_seen_hour = models.BigIntegerField(blank=True, null=True)
                    # year_weeknum = models.TextField(blank=True, null=True)
                    # iso_rep_year_wn = models.TextField(blank=True, null=True)

                    if program_in_db.type == "OTP":
                        program_in_db.age_group = "6-59m"
                    elif program_in_db.type == "SC":
                        program_in_db.age_group = program.values['age_group'].category

                    program_in_db.save()

                    # Drop duplicates
                    # if there is a duplicate for the same (siteid, type, weeknum, year) remove older report
                    for oldest_program_report in Program.objects.filter(
                        siteid=contact.siteid,
                        year=program_in_db.year,
                        weeknum=program_in_db.weeknum,
                        type=program_in_db.type).order_by('-last_seen')[1:]:

                        print("     Drop Duplicate")
                        oldest_program_report.delete()

                    a += 1
                    print(a)

        last_update_time.save()
# Ensure that amar_i and all other inpatients variables are included
