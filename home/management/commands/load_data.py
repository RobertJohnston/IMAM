# functions for data wrangling of imported dataframes.

import pandas as pd
import numpy as np

def rename_cols(dataframe):
    # edit the data in pandas

    # Registration database
    df.rename(columns={'Contact UUID': 'contact_uuid'}, inplace=True)
    df.rename(columns={'URN': 'urn'}, inplace=True)
    df.rename(columns={'Name': 'name'}, inplace=True)
    df.rename(columns={'Groups': 'groups'}, inplace=True)
    df.rename(columns={'SiteID': 'siteid'}, inplace=True)
    df.rename(columns={'Type': 'type'}, inplace=True)
    # Need to edit these date time variables to include Time Zone for Postgresql
    df.rename(columns={'First Seen': 'first_seen'}, inplace=True)
    df.rename(columns={'Last Seen': 'last_seen'}, inplace=True)
    # change variable name of the following
    df.rename(columns={'Mail (Value) - IMAM Register': 'mail'}, inplace=True)
    df.rename(columns={'Post_imp (Value) - IMAM Register': 'post'}, inplace=True)

    # Program database
    df.rename(columns={'WeekNum (Value) - IMAM Program': 'weeknum'}, inplace=True)
    df.rename(columns={'Role (Value) - IMAM Program': 'role'}, inplace=True)
    df.rename(columns={'Type (Value) - IMAM Program': 'type'}, inplace=True)
    df.rename(columns={'ProSiteID (Value) - IMAM Program': 'prositeid'}, inplace=True)
    df.rename(columns={'ProType (Value) - IMAM Program': 'protype'}, inplace=True)
    df.rename(columns={'age group (Value) - IMAM Program': 'age_group'}, inplace=True)
    # Outpatients admissions and exits
    df.rename(columns={'Beg_o (Value) - IMAM Program': 'beg'}, inplace=True)
    df.rename(columns={'Amar_o (Value) - IMAM Program': 'amar'}, inplace=True)
    df.rename(columns={'Tin_o (Value) - IMAM Program': 'tin'}, inplace=True)
    df.rename(columns={'Dcur_o (Value) - IMAM Program': 'dcur'}, inplace=True)
    df.rename(columns={'Dead_o (Value) - IMAM Program': 'dead'}, inplace=True)
    df.rename(columns={'DefU_o (Value) - IMAM Program': 'defu'}, inplace=True)
    df.rename(columns={'Dmed_o (Value) - IMAM Program': 'dmed'}, inplace=True)
    df.rename(columns={'Tout_o (Value) - IMAM Program': 'tout'}, inplace=True)
    # confirm correct data entry
    df.rename(columns={'Confirm (Category) - IMAM Program': 'confirm'}, inplace=True)

    # Stock database

    # LGA database

    return dataframe


merge_in_and_outpatients(dataframe):
    # convert admissions and exits to one column a piece not duplicates for out / in patients
    df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])

df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])
df['beg'] = np.where(df['type'] == "SC", df['Beg_i (Value) - IMAM Program'], df['beg'])



# df.rename(columns={'Beg_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Amar_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Tin_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Dcur_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Dcur_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Dead_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'DefU_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Dmed_i (Value) - IMAM Program': 'type'}, inplace=True)
# df.rename(columns={'Tout_i (Value) - IMAM Program': 'type'}, inplace=True)
# Confirmation of correct data entry

    return dataframe