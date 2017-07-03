from home.models import RawRegistration, Registration
from django.core.management.base import BaseCommand
from django.db import transaction

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

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):
        with transaction.atomic():
            Registration.objects.all().delete()
            a = RawRegistration.objects.all().count()

            for contact_row in RawRegistration.objects.all():
                a -= 1

                contact_in_db = Registration()

                contact_in_db.contact_uuid = contact_row.uuid

                contact_in_db.urn = contact_row.urn.lstrip('tel:')
                # contact_in_db.urn = contact_row.urn

                contact_in_db.name = contact_row.name.rstrip('.')
                contact_in_db.groups = contact_row.groups

                # if there is no siteid of contact then skip to next contact in contact_batch
                if not contact_row.siteid:
                    print("No siteid for %s (%s), skip" % (contact_row.name, repr(contact_row.siteid)))
                    continue
                # CHECK TYPE OF VARIABLE siteid HERE.
                # if siteid is a string, remove all letters from the string - in hopes to have only siteid numbers

                # Code below removes all text characters from siteid
                # this works well for examples such as siteid = 821110001 OTP"
                # Replaces upper and lower case letter Os with zeros

                if contact_row.siteid.isdigit():
                    contact_in_db.siteid = int(contact_row.siteid)
                else:
                    strip_siteid = filter(lambda x: x.isdigit(),
                                          contact_row.siteid.replace('O', '0').replace('o', '0'))
                    contact_in_db.siteid = int(strip_siteid)

                contact_in_db.type = contact_row.type
                contact_in_db.first_seen = contact_row.first_seen
                contact_in_db.last_seen = contact_row.last_seen
                contact_in_db.post = contact_row.post

                if not contact_row.mail or '@' not in contact_row.mail:
                    mail = None
                else:
                    mail = contact_row.mail.lower().rstrip('.').replace(' ', '').replace(',', '.')
                    # Data cleaning for email addresses - Change .con to .com
                    if mail.endswith('.con'):
                        mail = mail[:-1] + 'm'
                contact_in_db.mail = mail
                # contact_in_db.mail = contact_row.mail

                # Assign these from SiteID - do not import from RawRegistration.
                # state_num and lga_num

                if len(str(contact_row.siteid)) == 9 or len(str(contact_row.siteid)) == 3:
                    contact_in_db.state_num = int(str(contact_row.siteid)[:1])
                    contact_in_db.lga_num = int(str(contact_row.siteid)[:3])

                elif len(str(contact_row.siteid)) == 10 or len(str(contact_row.siteid)) == 4:
                    contact_in_db.state_num = int(str(contact_row.siteid)[:2])
                    contact_in_db.lga_num = int(str(contact_row.siteid)[:4])

                # State level
                elif len(str(contact_row.siteid)) == 1 or len(str(contact_row.siteid)) == 2:
                    contact_in_db.state_num = int(contact_row.siteid)
                    contact_in_db.lga_num = None

                else:
                    print(" SiteID ERROR-%s  UUID-%s  skipped" % (contact_row.siteid, contact_row.uuid))
                    continue



                print("count-%s  Name-%s" %(a, contact_in_db.name))
                contact_in_db.save()
