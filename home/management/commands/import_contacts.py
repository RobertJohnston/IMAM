from django.core.management.base import BaseCommand
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
            for contact in contact_batch:
                if Registration.objects.filter(contact_uuid=UUID(contact.uuid)).exists():
                    contact_in_db = Registration.objects.get(contact_uuid=UUID(contact.uuid))
                else:
                    contact_in_db = Registration()

                # Add index ? - Not used in analysis
                # Add contact_uuid
                # Add groups ?  Not used for anything except to identfy initial registration
                contact_in_db.urn = contact.urns[0]
                contact_in_db.name = contact.name
                contact_in_db.siteid = contact.fields['siteid']
                contact_in_db.type = contact.fields['type']
                # First Seen
                contact_in_db.first_seen = contact.created_on
                # Last Seen
                contact_in_db.last_seen = contact.modified_on
                contact_in_db.post = contact.fields['post']
                contact_in_db.mail = contact.fields['mail']

                contact_in_db.save()

                a += 1
                print(a)

# SiteID is forced above to be INT
# There will be many errors in SiteID.
# Need to make a list of all errors to present on the admin page to ensure that project manager will make corrections.

# Drop the contacts with siteid = NULL or NaN