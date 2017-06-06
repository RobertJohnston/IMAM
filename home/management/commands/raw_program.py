import json
from django import db
from home.models import Registration, JsonProgram, RawProgram
from django.core.management.base import BaseCommand
from django.db import transaction
# from isoweek import Week

# create model for RawProgram, make migrations, migrate

class Command(BaseCommand):
    help = 'Imports RawRegistration data from JsonRegistration'

    # A command must define handle
    def handle(self, *args, **options):
        with transaction.atomic():

            contact_cache = {}
            for contact in Registration.objects.all():
                contact_cache[contact.contact_uuid] = contact

            a = JsonProgram.objects.all().count()
            for json_program_row in JsonProgram.objects.all().iterator():
                # do this to avoid excessive memory consumption because django is
                # keeping track of every queries in memory for debugging purpose
                # according to memory_profile commenting out db.reset.queries() doesn't seems to change anything
                # db.reset_queries()

                id = json_program_row.id
                a -= 1

                #FIXME follow model in import contacts
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

                if "weeknum" not in json_data['values']:
                    print("Weeknum not in JSON data values for program data entry SKIPPED")
                    continue

                # Import contacts
                raw_program.contact_uuid = json_data['contact']['uuid']

                if raw_program.contact_uuid not in contact_cache:
                    # This is case with someone who has not completed registration but sends initial data
                    continue
                else:
                    contact = contact_cache[raw_program.contact_uuid]
                    raw_program.urn = contact.urn


                raw_program.name = json_data['contact']['name']
                # raw_program.groups

                # Role = Implementation or Supervision
                raw_program.role = json_data['values']['role']['category'] if 'role' in json_data['values'] else None
                raw_program.weeknum = json_data['values']['weeknum']['value'] if 'weeknum' in json_data['values'] else None

                # Normal data entry for implementation reports
                if "type" in json_data['values']:
                    raw_program.type = json_data['values']['type']['category']
                    raw_program.siteid = contact.siteid
                # Custom data entry for supervision program reports
                # if there is an entry in Protype (True) then supervisor sent data for implementation site
                elif "prositeid" in json_data['values']:
                    raw_program.siteid = json_data['values']['prositeid']['value']
                    raw_program.type = json_data['values']['protype']['category'] if 'protype' in json_data['values'] else None
                else:
                    raw_program.siteid = None
                    raw_program.type  = None


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

                print("countdown-%s" % a)
                raw_program.save()

