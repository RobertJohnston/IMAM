import time

from django.core.management.base import BaseCommand
from home.models import First_admin, Second_admin, Site

# Dependencies
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from temba_client.v2 import TembaClient

from django.conf import settings
from home.management.commands.load_data import rename_cols

# Refactor this export command

class Command(BaseCommand):
    help = 'Loads registration data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):

        client = TembaClient('rapidpro.io', open('token').read().strip())

        all_fields = set()
        for field_batch in client.get_fields().iterfetches(retry_on_rate_exceed=True):
            for field in field_batch:
                all_fields.add(field.key)

        # Export IMAM Supervision as xlsx file
        # Be careful with the correct indentation or this code will run before API load of contact data

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

        # Post ranking
        df2['post_rank'] = df2.post.str.lower()

        # Use replace with dictionary
        df2['post_rank'].replace({'coordinator': 1,
                                  'stocks manager': 2,
                                  'database manager': 3,
                                  'in charge hospital/phc': 4,
                                  'doctor': 5,
                                  'nurse/midwife': 6,
                                  'labtech-pharm': 7,
                                  'community health officer': 8,
                                  'volunteer': 9,
                                  'technical assistance': 10,
                                  'observer': 11},
                                 inplace=True)


        df2 = df2.query('siteid>1').query('siteid!=99')
        # Remove national level registrations
        # siteid == 99 is a number to use for missing or no longer involved with IMAM program
        # Remove erroneous registrations

        df2 = df2.sort_values(by=['siteid', 'post_rank', 'name'])

        # create db with only supervision staff
        supervision_df = df2[df2['siteid'] <= 3699]
        # supervision siteids range from 1 to 3699

        # to pivot data, create counts of each case by siteid
        # Remember that siteid == state_num or LGA_num if on supervision level.
        supervision_df.loc[:, 'count'] = supervision_df.groupby('siteid').cumcount() + 1

        # The data points to include in IMAM Supervision database for each supervision SiteID
        # Name, phone number, siteid, sitename, state(name), lga(name), state(supervision), lga(supervision)

        columnsTitles = ['name',
                         'num',
                         'siteid',
                         'mail',
                         'state_num',
                         'lga_num',
                         'count',
                         ]
        supervision_df = supervision_df.reindex(columns=columnsTitles)

        # create db with only State Level supervision staff
        first_admin = supervision_df[supervision_df['siteid'] <= 39]

        columnsTitles = ['name',
                         'num',
                         'siteid',
                         'mail',
                         'count',
                         ]
        first_admin = first_admin.reindex(columns=columnsTitles)

        # convert vertical to horizontal database.
        # will None in the cells cause us to send excessive number of warning SMS?
        first_admin_wide = first_admin.pivot(index='siteid', columns='count')

        # Create new column name
        # and correct multiIndex
        first_admin_wide.columns = ["sno" + str(first_admin_wide.columns[i][1]) + (first_admin_wide.columns[i][0]) for i
                                    in range(len(first_admin_wide.columns))]

        first_admin_wide = first_admin_wide.reset_index()

        # set index to be state_num - same as siteid for state
        first_admin_wide = first_admin_wide.set_index('siteid')
        # remove name of index
        first_admin_wide.index.name = None

        # Test for correct phone numbers in merge
        assert True not in first_admin_wide['sno1num'].isnull().value_counts().keys()

        # Add first_admin_wide to first_admin to merge to IMAM supervision df later
        first_admin = first_admin.drop('count', axis=1)

        # Use column space for sitename
        first_admin.rename(columns={'mail': 'sitename'}, inplace=True)

        # Add site name from postgres
        first_admin['sitename'] = first_admin['siteid'].map(
            lambda x: First_admin.objects.get(state_num=x).state.strip() if First_admin.objects.filter(
                state_num=x) else "")

        first_admin = pd.merge(first_admin, first_admin_wide, left_on='siteid', right_index=True, how='left',
                               sort=False)

        # Create same list for LGA
        # create db with only LGA Level supervision staff
        second_admin = supervision_df.query('siteid>=101').query('siteid<=3699')

        columnsTitles = ['name',
                         'num',
                         'siteid',
                         'mail',
                         'count',
                         ]
        second_admin = second_admin.reindex(columns=columnsTitles)

        # convert vertical to horizontal database.
        second_admin_wide = second_admin.pivot(index='siteid', columns='count')

        # Rename columns and correct multiIndex
        second_admin_wide.columns = ["lga" + str(second_admin_wide.columns[i][1]) + (second_admin_wide.columns[i][0])
                                     for i in range(len(second_admin_wide.columns))]

        second_admin_wide = second_admin_wide.reset_index()

        # Add second_admin_wide to second_admin to merge to IMAM supervision df later
        second_admin = second_admin.drop('count', axis=1)

        # Use column space for sitename
        second_admin.rename(columns={'mail': 'sitename'}, inplace=True)

        # Add site name from postgres
        second_admin['sitename'] = second_admin['siteid'].map(
            lambda x: Second_admin.objects.get(lga_num=x).lga.strip() + " LGA" if Second_admin.objects.filter(
                lga_num=x) else "")


        # Add state_num to LGA df
        second_admin_wide['state_num'] = 0

        # Recode state_num to LGA df
        second_admin_wide['state_num'] = np.where(second_admin_wide['siteid'] < 3699,
                                                  second_admin_wide['siteid'].astype(str).str[:2],
                                                  second_admin_wide['state_num'])
        second_admin_wide['state_num'] = np.where(second_admin_wide['siteid'] < 999,
                                                  second_admin_wide['siteid'].astype(str).str[:1],
                                                  second_admin_wide['state_num'])


        # Do not forget to cast state_num to INT or merge will not work
        second_admin_wide['state_num'] = second_admin_wide['state_num'].astype(int)

        first_second = pd.merge(second_admin_wide, first_admin_wide, left_on='state_num', right_index=True, how='left',
                                sort=False)

        # Test for correct phone numbers in merge
        assert True not in first_second['sno1num'].isnull().value_counts().keys()
        assert True not in first_second['lga1num'].isnull().value_counts().keys()

        # can convert this to SiteID later.
        first_second['lga_num'] = first_second['siteid']

        # Merge first_second to second_admin to append to IMAM Supervision
        second_admin = pd.merge(second_admin, first_second, left_on='siteid', right_on='siteid', how='left', sort=False)
        # Check suffixes

        # Test for correct phone numbers in merge
        assert True not in second_admin['sno1num'].isnull().value_counts().keys()
        assert True not in second_admin['lga1num'].isnull().value_counts().keys()

        # merge to implementation staff df
        site = df2.query('siteid > 3699')

        # Drop data with no lga_num - this deletes entire row where a NaN is found
        site = site.query('lga_num==lga_num')

        # Change the order (the index) of the columns
        columnsTitles = ['name',
                         'num',
                         'siteid',
                         'sitename',
                         'lga_num',
                         'state_num'
                         ]

        site = site.reindex(columns=columnsTitles)

        imam_supervision = pd.merge(site, first_second, left_on='lga_num', right_on='lga_num', how='right',
                                    suffixes=('', '_y'), sort=False)

        # Test for correct phone numbers in merge
        assert True not in second_admin['sno1num'].isnull().value_counts().keys()
        assert True not in second_admin['lga1num'].isnull().value_counts().keys()


        imam_supervision.drop('siteid_y', axis=1, inplace=True)

        imam_supervision = imam_supervision.sort_values(by=['siteid', 'name'])

        # Change the order (the index) of the columns
        columnsTitles = ['name',
                         'num',
                         'siteid',
                         'sitename',
                         'lga_num',
                         'state_num'
                         ]
        site = site.reindex(columns=columnsTitles)

        # TODO somehow the merge procuded situation where the siteid can be NaN and that breaked everything
        # this is probably du to non matching data
        imam_supervision = imam_supervision.query('siteid == siteid')

        # add sitenames
        imam_supervision['sitename'] = imam_supervision['siteid'].map(
            lambda x: Site.objects.get(siteid=x).sitename.strip() if Site.objects.filter(siteid=x) else "")

        # Append first_admin & second_admin to site level
        final_df = second_admin.append(first_admin).append(imam_supervision)

        # Drop state_num lga_num state_num_y
        final_df = final_df.drop(['state_num', 'lga_num', 'state_num_y'], axis=1)

        # Change num to Phone to match RapidPro variable name.
        final_df.rename(columns={'num': 'Phone'}, inplace=True)


        # convert to xls and/or export as JSON
        # Test Export as Excel
        filename = "IMAM_supervision.xlsx"
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        final_df.to_excel(writer, 'Sheet1')
        writer.save()
        writer.close()

        print('IMAM_Supervision.xlsx exported')

        # this will give use all the column names into a set
        all_needed_fields = set(final_df) - {'name', 'Phone', 'siteid', 'sitename'}

        for field_to_create in all_needed_fields - all_fields:
            print "Creating new needed field:", field_to_create
            client.create_field(label=field_to_create, value_type='text')

        def update_contact_fields(row_in_df):
            new_contact_fields = {}

            for field in all_needed_fields:
                if row_in_df[field] and row_in_df[field] == row_in_df[field]:
                    new_contact_fields[field] = row_in_df[field]
                else:
                    new_contact_fields[field] = ''

            print row_in_df.name, row_in_df['name'], row_in_df['Phone'], new_contact_fields
            client.update_contact('tel:' + row_in_df['Phone'], fields=new_contact_fields)

            # make is slow so we don't exceed rate limit
            time.sleep(1)

            # time to complete export_imam_supervision.py
            # 1:45 minutes

        final_df.apply(update_contact_fields, axis=1)
