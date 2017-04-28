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

                    # we know that those contacts are broken because they don't have a valid siteid so we skip them
                    if contact.uuid in ('2e3ab6f7-4bff-411d-9565-fc174a57a7de',
                                        '980369db-7e03-41d0-8f73-3909fda60e6e',
                                        '1112aee2-471a-4a20-8907-0bd25299e515'):
                        continue

                    # Update contact
                    if Registration.objects.filter(contact_uuid=UUID(contact.uuid)).exists():
                        contact_in_db = Registration.objects.get(contact_uuid=UUID(contact.uuid))
                    # Create new contact
                    else:
                        contact_in_db = Registration()
                        contact_in_db.contact_uuid = UUID(contact.uuid)

                    # if there is no siteid of contact then skip to next contact in contact_batch
                    if not contact.fields['siteid']:
                        print ("No siteid for %s, skip" % contact.name)
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
                        strip_siteid = filter(lambda x: x.isdigit(), contact.fields['siteid'].replace('O', '0').replace('o', '0'))
                        contact_in_db.siteid = int(strip_siteid)

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

                    # Create state_num and LGA_num
                    # Implementation and LGA level
                    if len(str(contact_in_db.siteid)) == 9 or len(str(contact_in_db.siteid)) == 3:
                        contact_in_db.state_num = int(str(contact_in_db.siteid)[:1])
                        contact_in_db.lga_num = int(str(contact_in_db.siteid)[:3])

                    elif len(str(contact_in_db.siteid)) == 10 or len(str(contact_in_db.siteid)) == 4:
                        contact_in_db.state_num = int(str(contact_in_db.siteid)[:2])
                        contact_in_db.lga_num = int(str(contact_in_db.siteid)[:4])

                    # State level
                    elif len(str(contact_in_db.siteid)) == 1 or len(str(contact_in_db.siteid)) == 2:
                        contact_in_db.state_num = int(contact_in_db.siteid)
                        contact_in_db.lga_num = None

                    else:
                        raise Exception()

                    contact_in_db.save()

                    a += 1
                    print(a)

# SiteID is forced above to be INT
# There will be many errors in SiteID.
# Need to make a list of all errors to present on the admin page to ensure that project manager will make corrections.

# Drop the contacts with siteid = NULL or NaN