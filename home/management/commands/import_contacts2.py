from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import RawRegistration, Registration, LastUpdatedAPICall

from home.utilities import exception_to_sentry

# Import contacts from RawRegistration
# NOTE
# RapidPro manages the contacts so that there is only one contact per phone number.
# Currently, we do not need to sort and take the most recent entry.
# If we find that there have been a lot of changes of SiteID in contacts over time, then we will need to import the
# runs of the Registration flow and record the data of change of the SiteID. From the date of change of SiteID,
# we will stitch together the data from the beginning of the data collection.

class Command(BaseCommand):
    help = 'Loads contact data to from raw contacts to clean contacts'

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

            last_update_time = LastUpdatedAPICall.objects.filter(kind="contacts2").first()

            counter= RawRegistration.objects.all().count()

            # Code below is explicitly describing all possible four conditions of two booleans
            if options['all'] and last_update_time:
                Registration.objects.all().delete()
                data_to_process = RawRegistration.objects.all()

            elif options['all'] and not last_update_time:
                Registration.objects.all().delete()
                data_to_process = RawRegistration.objects.all()
                last_update_time = LastUpdatedAPICall(kind="contacts2")

            elif not options['all'] and last_update_time:
                # Start from end of attempt to load data: GET all data since timestamp of last time
                # remember to use modified_on not last seen
                data_to_process = RawRegistration.objects.filter(modified_on__gte=last_update_time.timestamp)
                counter = RawRegistration.objects.filter(modified_on__gte=last_update_time.timestamp).count()

            elif not options['all'] and not last_update_time:
                Registration.objects.all().delete()
                data_to_process = RawRegistration.objects.all()
                last_update_time = LastUpdatedAPICall(kind="contacts2")
            else:
                raise Exception()
                # This is unncessary in this context but good programming practice

            last_update_time.timestamp = datetime.now()

            for row in data_to_process.iterator():
                id = row.uuid
                counter -= 1

                # Update contact if id exists in Registration.objects
                if Registration.objects.filter(contact_uuid=id):
                    contact_in_db = Registration.objects.get(contact_uuid=id)

                # Create contact if id does not exist already
                else:
                    contact_in_db = Registration()
                    contact_in_db.contact_uuid = id

                contact_in_db.urn = row.urn.lstrip('tel:')
                contact_in_db.name = row.name.rstrip('.')
                contact_in_db.groups = row.groups

                # if there is no siteid of contact then skip to next contact in contact_batch
                if not row.siteid:
                    print("No siteid for %s (%s), skip" % (row.name, repr(row.siteid)))
                    continue

                # CHECK TYPE OF VARIABLE siteid HERE.
                # if siteid is a string, remove all letters from the string - in hopes to have only siteid numbers
                # Code below removes all text characters from siteid
                # this works well for examples such as siteid = 821110001 OTP"
                # Replaces upper and lower case letter Os with zeros

                if row.siteid.isdigit():
                    contact_in_db.siteid = int(row.siteid)
                else:
                    strip_siteid = filter(lambda x: x.isdigit(),
                                          row.siteid.replace('O', '0').replace('o', '0'))
                    contact_in_db.siteid = int(strip_siteid)

                contact_in_db.type = row.type
                contact_in_db.first_seen = row.first_seen
                contact_in_db.last_seen = row.last_seen
                contact_in_db.post = row.post

                if not row.mail or '@' not in row.mail:
                    mail = None
                else:
                    mail = row.mail.lower().rstrip('.').replace(' ', '').replace(',', '.')
                    # Data cleaning for email addresses - Change .con to .com
                    if mail.endswith('.con'):
                        mail = mail[:-1] + 'm'
                contact_in_db.mail = mail
                # contact_in_db.mail = row.mail

                # Assign these from SiteID - do not import from RawRegistration.
                # state_num and lga_num

                if len(str(row.siteid)) == 9 or len(str(row.siteid)) == 3:
                    contact_in_db.state_num = int(str(row.siteid)[:1])
                    contact_in_db.lga_num = int(str(row.siteid)[:3])

                elif len(str(row.siteid)) == 10 or len(str(row.siteid)) == 4:
                    contact_in_db.state_num = int(str(row.siteid)[:2])
                    contact_in_db.lga_num = int(str(row.siteid)[:4])

                # State level
                elif len(str(row.siteid)) == 1 or len(str(row.siteid)) == 2:
                    contact_in_db.state_num = int(row.siteid)
                    contact_in_db.lga_num = None

                else:
                    print(" SiteID ERROR-%s  UUID-%s  skipped" % (row.siteid, row.uuid))
                    continue

                print("Contacts count-%s  Name-%s" %(counter, contact_in_db.name))
                contact_in_db.save()

            last_update_time.save()