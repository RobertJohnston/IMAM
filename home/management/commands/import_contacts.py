from django.core.management.base import BaseCommand
from django.db import transaction
from temba_client.v2 import TembaClient
from home.models import Registration

from uuid import UUID

# to run python manage.py import_program

class Command(BaseCommand):
    help = 'Loads registration data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        client = TembaClient('rapidpro.io', open('token').read().strip())

        a = 0
        for contact_batch in client.get_contacts(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True):
            with transaction.atomic():
                for contact in contact_batch:
                    # Optimization tool - transaction.atomic -is turned on

                    # Update contact
                    if Registration.objects.filter(contact_uuid=UUID(contact.uuid)).exists():
                        contact_in_db = Registration.objects.get(contact_uuid=UUID(contact.uuid))
                    # Create new contact
                    else:
                        contact_in_db = Registration()
                        contact_in_db.contact_uuid = UUID(contact.uuid)

                    # if there is no siteid of contact then skip to next contact in contact_batch
                    if not contact.fields['siteid']:
                        print "No siteid for %s, skip" % contact.name
                        continue

                    contact_in_db.urn = contact.urns[0]
                    contact_in_db.name = contact.name

                    # CHECK TYPE OF VARIABLE siteid HERE.
                    # if siteid is a string, remove all letters from the string - in hopes to have only siteid numbers

                    # Code below removes all text characters from siteid
                    # this works well for examples such as siteid = 821110001 OTP"
                    # it does not work for siteid = 82111ooo1" - these contact entries are dropped.

                    try:
                        contact_in_db.siteid = int(contact.fields['siteid'])
                        # contact.fields['siteid'].isalnum ?
                    except ValueError:
                        strip_siteid = filter(lambda x: x.isdigit(), contact.fields['siteid'])
                        contact_in_db.siteid = strip_siteid

                    contact_in_db.type = contact.fields['type']
                    # First Seen
                    contact_in_db.first_seen = contact.created_on
                    # Last Seen
                    contact_in_db.last_seen = contact.modified_on
                    contact_in_db.post = contact.fields['post']

                    if not contact.fields['mail'] or '@' not in contact.fields["mail"]:
                        mail = None
                    else:
                        mail = contact.fields["mail"].lower().rstrip('.').replace(' ', '').replace(',', '.')

                        if mail.endswith('.con'):
                            mail = mail[:-1] + 'm'

                    contact_in_db.mail = mail

                    contact_in_db.save()

                    a += 1
                    print(a)

# SiteID is forced above to be INT
# There will be many errors in SiteID.
# Need to make a list of all errors to present on the admin page to ensure that project manager will make corrections.

# Drop the contacts with siteid = NULL or NaN