import json
from django import db
from home.models import Registration, JsonProgram, RawProgram, LastUpdatedAPICall
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime
# from isoweek import Week
from home.utilities import exception_to_sentry


class Command(BaseCommand):
    help = 'Imports RawProgram data from JsonProgram'

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

            last_update_time = LastUpdatedAPICall.objects.filter(kind="raw_program").first()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                RawProgram.objects.all().delete()
                data_to_process = JsonProgram.objects.all()

            elif options['all'] and not last_update_time:
                RawProgram.objects.all().delete()
                data_to_process = JsonProgram.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_program")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                data_to_process = JsonProgram.objects.filter(modified_on__gte=last_update_time.timestamp)

            elif not options['all'] and not last_update_time:
                RawProgram.objects.all().delete()
                data_to_process = JsonProgram.objects.all()
                last_update_time = LastUpdatedAPICall(kind="raw_program")

            last_update_time.timestamp = datetime.now()

            # Change to countdown
            counter= JsonProgram.objects.all().count()

            contact_cache = {}
            for contact in Registration.objects.all():
                contact_cache[contact.contact_uuid] = contact

            for json_program_row in data_to_process.iterator():
                # Use db.reset queries - to avoid excessive memory consumption because django is
                # keeping track of every queries in memory for debugging purpose
                # according to memory_profile commenting out db.reset.queries() doesn't seems to change anything
                # db.reset_queries()

                id = json_program_row.id
                counter-= 1

                # Update program
                if RawProgram.objects.filter(id=id):
                    # print("update Program id %s" % id)
                    raw_program = RawProgram.objects.get(id=id)
                # Create contact
                else:
                    # print("create Program id %s" % id)
                    raw_program = RawProgram()
                    raw_program.id = id

                # Create api_data from json_program_row to import to RawProgram
                json_data = json.loads(json_program_row.json)

                # if "weeknum" not in json_data['values']:
                #     print("Weeknum not in JSON data values for program data entry SKIPPED")
                #     # Data entries where Pro was selected but there are no data entered.
                #     continue

                # Import contacts
                # This is not a set attribute error because we are not using a var or object to represent the data
                raw_program.contact_uuid = json_data['contact']['uuid']

                if raw_program.contact_uuid not in contact_cache:
                    # This is case with someone who has not completed registration but sends initial data
                    continue
                else:
                    contact = contact_cache[raw_program.contact_uuid]
                    raw_program.urn = contact.urn


                raw_program.name = json_data['contact']['name']
                # raw_program.groups

                # Role = Implementation or Supervision - this is unncessary to collect
                raw_program.role = json_data['values']['role']['category'] if 'role' in json_data['values'] else None
                raw_program.weeknum = json_data['values']['weeknum']['value'] if 'weeknum' in json_data['values'] else None

                # Normal data entry for implementation reports
                if "type" in json_data['values']:
                    raw_program.type = json_data['values']['type']['category']

                    # Data stitching to integrate SITEID is working in raw_program since 8th June 2017
                    if 'siteid' in json_data['values'] and isinstance(json_data['values']['siteid']['value'], (int, float)):
                        raw_program.siteid = json_data['values']['siteid']['value']
                        print raw_program.siteid
                    # code below brings siteid from contacts for old data entries before the corrections in RapidPro
                    else:
                        raw_program.siteid = contact.siteid

                # Custom data entry for supervision program reports
                # if there is an entry in Protype (True) then supervisor sent data for implementation site
                elif "prositeid" in json_data['values']:
                    raw_program.siteid = json_data['values']['prositeid']['value']
                    raw_program.type = json_data['values']['protype']['category'] if 'protype' in json_data['values'] else None
                else:
                    raw_program.siteid = None
                    raw_program.type  = None

                #FIXME - make more explicit
                # def clean(value_to_clean):
                #     try:
                #         return int(float(value_to_clean))
                #     except ValueError:
                #         print("Fail to convert '%s' as a number" % (value_to_clean))
                #         return None

                # Data cleaning for inpatients and outpatients
                # program_in_db.weeknum = clean(program_row.weeknum)


                # OUTPATIENTS
                if raw_program.type == "OTP" :
                    raw_program.age_group = "6-59m"
                    varlist = ('beg_o', 'amar_o', 'tin_o', 'dcur_o', 'dead_o', 'defu_o', 'dmed_o', 'tout_o')

                # INPATIENTS
                elif raw_program.type == "SC":
                    raw_program.age_group = json_data['values']['age_group']['category'] if 'age_group' in json_data[
                        'values'] else None
                    varlist = ('beg_i', 'amar_i', 'tin_i', 'dcur_i', 'dead_i', 'defu_i', 'dmed_i', 'tout_i')

                else:
                    varlist = ()

                for var in varlist:
                    raw_var = var[:-2]
                    setattr(raw_program, raw_var, json_data['values'][var]['value']\
                        if var in json_data['values'] else None)


                raw_program.first_seen = json_data['created_on']
                raw_program.last_seen = json_data['modified_on']

                raw_program.confirm = json_data['values']['confirm']['category']  if 'confirm' in json_data['values'] else None

                # state_num
                # lga_num
                # year

                # last_seen_weeknum
                # rep_year_wn
                # rep_weeknum
                # last_seen_dotw
                # last_seen_hour
                # year_weeknum
                # iso_rep_year_wn
                # iso_year_weeknum
                # iso_diff
                # since_x_weeks = models.BigIntegerField(blank=True, null=True)

                print("countdown-%s" % counter)
                raw_program.save()


        last_update_time.save()
