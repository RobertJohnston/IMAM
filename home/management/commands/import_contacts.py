from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from temba_client.v2 import TembaClient
from home.models import Registration, LastUpdatedAPICall, First_admin, Second_admin, Site

from uuid import UUID

# Dependencies
import pandas as pd
import numpy as np
import xlsxwriter
from pandas import ExcelWriter

from sqlalchemy import create_engine


from django.conf import settings
from home.management.commands.load_data import rename_cols


# to run python manage.py (name of file), OR
# ipython --pdb manage.py (name of file)


class Command(BaseCommand):
    help = 'Loads registration data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):
        client = TembaClient('rapidpro.io', open('token').read().strip())

        # Check in PostGreSQL database for last timestamp of API call
        last_update_time = LastUpdatedAPICall.objects.filter(kind="contact").first()

        if last_update_time:
            clients_from_api = client.get_contacts(group='Nut Personnel', after=last_update_time.timestamp)
        else:
            clients_from_api = client.get_contacts(group='Nut Personnel')
            last_update_time = LastUpdatedAPICall(kind="contact")

        last_update_time.timestamp = datetime.now()

        a = 0
        for contact_batch in clients_from_api.iterfetches(retry_on_rate_exceed=True):
            # Optimization tool - transaction.atomic -is turned on
            with transaction.atomic():
                for contact in contact_batch:

                    # we know that those contacts are broken because they don't have a valid siteid so we skip them
                    if contact.uuid in ('2e3ab6f7-4bff-411d-9565-fc174a57a7de',
                                        '980369db-7e03-41d0-8f73-3909fda60e6e',
                                        '1112aee2-471a-4a20-8907-0bd25299e515'):
                        continue

                    # Update contact
                    if Registration.objects.filter(contact_uuid=UUID(contact.uuid)).exists():
                        contact_in_db = Registration.objects.get(contact_uuid=UUID(contact.uuid))
                        print('     Update existing contact')
                    # Create new contact
                    else:
                        contact_in_db = Registration()
                        contact_in_db.contact_uuid = UUID(contact.uuid)
                        print('Creating a new contact')

                    # if there is no siteid of contact then skip to next contact in contact_batch
                    if not contact.fields['siteid']:
                        print ("No siteid for %s, skip" % contact.name)
                        continue

                    contact_in_db.urn = contact.urns[0].lstrip('tel:')
                    contact_in_db.name = contact.name

                    # CHECK TYPE OF VARIABLE siteid HERE.
                    # if siteid is a string, remove all letters from the string - in hopes to have only siteid numbers

                    # Code below removes all text characters from siteid
                    # this works well for examples such as siteid = 821110001 OTP"
                    # Replaces upper and lower case letter Os with zeros

                    if contact.fields['siteid'].isdigit():
                        contact_in_db.siteid = int(contact.fields['siteid'])

                    else:
                        strip_siteid = filter(lambda x: x.isdigit(), contact.fields['siteid'].replace('O', '0').replace('o', '0'))
                        contact_in_db.siteid = int(strip_siteid)

                    contact_in_db.type = contact.fields['type']
                    # First Seen
                    contact_in_db.first_seen = contact.created_on
                    # Last Seen
                    contact_in_db.last_seen = contact.modified_on
                    contact_in_db.post = contact.fields['post']

                    # This code was used for an error in RapidPro in Nov 2016 to correct presentation of post
                    # it is no longer necessary.
                    # if contact.fields['post'] == "S":
                    #     contact_in_db.post ="STOCKS MANAGER"
                    # if contact.fields['post'] == "D":
                    #     contact_in_db.post = "DATABASE MANAGER"

                    if not contact.fields['mail'] or '@' not in contact.fields["mail"]:
                        mail = None
                    else:
                        mail = contact.fields["mail"].lower().rstrip('.').replace(' ', '').replace(',', '.')

                        # Data cleaning for email addresses - Change .con to .com
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

        last_update_time.save()