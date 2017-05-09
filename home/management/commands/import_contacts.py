from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from temba_client.v2 import TembaClient
from home.models import Registration, LastUpdatedAPICall

from uuid import UUID

# to run python manage.py import_program

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

                    contact_in_db.urn = contact.urns[0]
                    contact_in_db.name = contact.name

                    # CHECK TYPE OF VARIABLE siteid HERE.
                    # if siteid is a string, remove all letters from the string - in hopes to have only siteid numbers

                    # Code below removes all text characters from siteid
                    # this works well for examples such as siteid = 821110001 OTP"
                    # Replaces upper and lower case letter Os with zeros

                    try:
                        contact_in_db.siteid = int(contact.fields['siteid'])

                    except ValueError:
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

        # SiteID in RapidPro is forced to be INT
        # all entries with letters are rejected

        # If we have errors in SiteID, make a list of errors to present on the admin page
        # to ensure that project manager will make corrections.

        # Drop the contacts with siteid = NULL or NaN


        # Export IMAM Supervision as xlsx file

        # Dependencies
        import pandas as pd
        import numpy as np
        from pandas import ExcelWriter
        import xlsxwriter
        from sqlalchemy import create_engine
        from django.conf import settings

        import os
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMAM.settings")

        from django.conf import settings
        from home.management.commands.load_data import rename_cols, generic_cleaning
        # FIXME
        from home.models import First_admin, Second_admin, Site, Registration

        # Load in contact database
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
        df = pd.read_sql_query("select * from registration;", con=engine)

        # run rename columns function
        rename_cols(df)

        # CHANGE URN TO NUM
        df = df.rename(index=str, columns={"urn": "num"})

        # Change the order (the index) of the columns
        columnsTitles = ['siteid',
                         'name',
                         'num',
                         'mail',
                         'post',
                         'type',
                         'first_seen',
                         'last_seen',
                         'lga_num',
                         'state_num'
                         ]

        df2 = df.reindex(columns=columnsTitles)

        # Post ranking (to put state nutrition officers first and technical assistance last)
        df2['post_rank'] = df2.post.str.lower()
        df2['post_rank'].replace({'coordinator':            1,
                                  'stocks manager':         2,
                                  'database manager':       3,
                                  'in charge hospital/phc': 4,
                                  'doctor':                 5,
                                  'nurse/midwife':          6,
                                  'labtech-pharm':          7,
                                  'community health officer': 8,
                                  'volunteer':              9,
                                  'technical assistance':   10,
                                  'observer':               11},
                                  inplace=True)

        # change type in supervision cadres to "Sup"
        df2['type'] = np.where((df2['siteid']) < 3699, "Sup", df2['type'])

        df2 = df2.query('siteid>1').query('siteid!=99')
        # Remove national level registrations
        # siteid == 99 is a number to use for missing or no longer involved with IMAM program
        # Remove erroneous registrations

        df2 = df2.sort_values(by=['siteid', 'post_rank', 'name'])

        # create db with only supervision staff (siteids range from 1 to 3699 all first and second admin)
        # Instead of hard coding number - put max of second admin
        supervision_df = df2[df2['siteid'] <= 3699]

        # to pivot data, create counts of each case by siteid
        # Remember that siteid == state_num or LGA_num if on supervision level.
        supervision_df.loc[:, 'count'] = supervision_df.groupby('siteid').cumcount() + 1

        # The data points to include in IMAM Supervision database for each supervision SiteID
        # Name, phone number, email
        # can remove state_num and lga_num
        columnsTitles = ['siteid',
                         'name',
                         'num',
                         'mail',
                         'count',
                         ]

        supervision_df = supervision_df.reindex(columns=columnsTitles)

        # add names to first admin level
        # FIXME
        # supervision_df.loc[:, 'sitename'] = supervision_df['siteid'].map(
        #     lambda x: First_admin.objects.get(state_num=x).state.strip() if First_admin.objects.filter(state_num=x) else "")
        # # add names to second admin level
        # supervision_df.loc[:, 'sitename'] = supervision_df['siteid'].map(
        #     lambda x: Second_admin.objects.get(lga_num=x).lga.strip() + " LGA" if Second_admin.objects.filter(lga_num=x) else "")

        # Change None in cells to blank
        # for cell in lga:
        #   lga[cell].fillna(value='', inplace=True)

        # Ensure that we have
        # NAME, Phone, SiteID, SiteName, State(name), LGA(name), SNO supervision, LGA supervision

        # SUPERVISION_DF - Final


        # create db with only State Level supervision staff
        # Instead of hard coding number - put max of first admin
        state_df = supervision_df[supervision_df['siteid'] <= 39]

        # convert vertical to horizontal database.
        # will None in the cells cause us to send excessive number of warning SMS?
        state_wide = state_df.pivot(index='siteid', columns='count')

        # Create new column name
        # and correct multiIndex
        state_wide.columns = ["sno" + str(state_wide.columns[i][1]) + (state_wide.columns[i][0]) for i in
                              range(len(state_wide.columns))]

        state = state_wide.reset_index()

        # set index to be state_num - same as siteid for state
        state = state.set_index('siteid')
        # remove name of index
        state.index.name = None


        # Create same list for LGA
        # create db with only LGA Level supervision staff
        # replace lower and upper limits with min and max of 2nd admin
        lga_df = supervision_df.query('siteid>=101').query('siteid<=3699')

        # convert vertical to horizontal database.
        # will None in the cells cause us to send excessive number of warning SMS?
        lga_wide = lga_df.pivot(index='siteid', columns='count')

        # Rename columns and correct multiIndex
        lga_wide.columns = ["lga" + str(lga_wide.columns[i][1]) + (lga_wide.columns[i][0]) for i in
                            range(len(lga_wide.columns))]

        lga = lga_wide.reset_index()

        lga['state_num'] = 0
        # Add state_num to LGA df
        lga['siteid_lgt'] = lga['siteid'].astype(str).str.len()

        lga['state_num'] = np.where(lga['siteid_lgt'] == 3, lga['siteid'].astype(str).str[:1], lga['state_num'])
        lga['state_num'] = np.where(lga['siteid_lgt'] == 4, lga['siteid'].astype(str).str[:2], lga['state_num'])
        lga = lga.drop('siteid_lgt', axis=1)

        # cast state_num to INT or merge will not work
        lga['state_num'] = lga['state_num'].astype(int)
        lga['state_num'].value_counts()

        # Merge state level supervision data into LGA data
        imam_sup = pd.merge(lga, state, left_on='state_num', right_index=True, how='left', sort=False)

        # SiteID is now NaN for state.
        # can convert this to SiteID later.
        imam_sup['lga_num'] = imam_sup['siteid']

        # merge to implementation staff df
        imam_imp = df2.query('siteid > 3699')
        imam_imp.siteid.value_counts()

        # Change the order (the index) of the columns
        columnsTitles = ['name',
                         'num',
                         'siteid',
                         'lga_num',
                         'state_num'
                         ]

        imam_imp = imam_imp.reindex(columns=columnsTitles)

        # merge supervision df to implementation df
        imam_supervision = pd.merge(imam_imp, imam_sup, left_on='lga_num', right_on='lga_num', how='left',
                                    suffixes=('_x', '_y'), sort=False)

        # Test for correct merge
        # FIXME
        # assert
        # imam_supervision.sno1urn.value_counts()
        # assert
        # imam_supervision.lga1urn.value_counts()


        # add names to site level
        # FIXME
        # imam_supervision['sitename'] = imam_supervision['siteid_x'].map(
        #     lambda x: Site.objects.get(siteid=x).sitename.strip() if Site.objects.filter(siteid=x) else "")

        # clean all column names

        # convert to xls and/or export as JSON
        filename = "IMAM_supervision.xlsx"
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        imam_sup.to_excel(writer, 'Sheet1')
        writer.save()
        writer.close()






