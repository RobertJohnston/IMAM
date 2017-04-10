from django.core.management.base import BaseCommand
from django.conf import settings
from temba_client.v2 import TembaClient

from home.models import Registration

from uuid import UUID

# to run python manage.py load_data

# STOCKS DATA

class Command(BaseCommand):
    help = 'Loads data to SQL for IMAM website'

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

                contact_in_db.urn = contact.urns[0]
                contact_in_db.name = contact.name
                contact_in_db.siteid = contact.fields['siteid']
                contact_in_db.type = contact.fields['type']
                contact_in_db.last_seen = contact.modified_on
                contact_in_db.post = contact.fields['post']
                contact_in_db.mail = contact.fields['mail']

                contact_in_db.save()

                a += 1
                print(a)