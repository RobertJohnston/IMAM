# functions for data wrangling of imported dataframes.

import pandas as pd
import numpy as np

def rename_cols(dataframe):
    # edit the data in pandas

    # Registration database
    dataframe.rename(columns={'Contact UUID': 'contact_uuid'}, inplace=True)
    dataframe.rename(columns={'URN': 'urn'}, inplace=True)
    dataframe.rename(columns={'Name': 'name'}, inplace=True)
    dataframe.rename(columns={'Groups': 'groups'}, inplace=True)
    dataframe.rename(columns={'SiteID': 'siteid'}, inplace=True)
    dataframe.rename(columns={'Type': 'type'}, inplace=True)
    # Need to edit these date time variables to include Time Zone for Postgresql
    dataframe.rename(columns={'First Seen': 'first_seen'}, inplace=True)
    dataframe.rename(columns={'Last Seen': 'last_seen'}, inplace=True)
    # change variable name of the following
    dataframe.rename(columns={'Mail (Value) - IMAM Register': 'mail'}, inplace=True)
    dataframe.rename(columns={'Post_imp (Value) - IMAM Register': 'post'}, inplace=True)

    # Program database
    dataframe.rename(columns={'WeekNum (Value) - IMAM Program': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'Role (Value) - IMAM Program': 'role'}, inplace=True)
    dataframe.rename(columns={'Type (Category) - IMAM Program': 'type'}, inplace=True)
    dataframe.rename(columns={'ProSiteID (Value) - IMAM Program': 'prositeid'}, inplace=True)
    dataframe.rename(columns={'ProType (Value) - IMAM Program': 'protype'}, inplace=True)
    dataframe.rename(columns={'age group (Value) - IMAM Program': 'age_group'}, inplace=True)
    # Outpatients admissions and exits
    dataframe.rename(columns={'Beg_o (Value) - IMAM Program': 'beg'}, inplace=True)
    dataframe.rename(columns={'Amar_o (Value) - IMAM Program': 'amar'}, inplace=True)
    dataframe.rename(columns={'Tin_o (Value) - IMAM Program': 'tin'}, inplace=True)
    dataframe.rename(columns={'Dcur_o (Value) - IMAM Program': 'dcur'}, inplace=True)
    dataframe.rename(columns={'Dead_o (Value) - IMAM Program': 'dead'}, inplace=True)
    dataframe.rename(columns={'DefU_o (Value) - IMAM Program': 'defu'}, inplace=True)
    dataframe.rename(columns={'Dmed_o (Value) - IMAM Program': 'dmed'}, inplace=True)
    dataframe.rename(columns={'Tout_o (Value) - IMAM Program': 'tout'}, inplace=True)
    # confirm correct data entry
    dataframe.rename(columns={'Confirm (Category) - IMAM Program': 'confirm'}, inplace=True)

    # Stock database

    # LGA database

    return dataframe


def merge_in_and_outpatients(dataframe):
    # convert admissions and exits to one column a piece not duplicates for out / in patients
    dataframe['beg'] = np.where(dataframe['type'] == "SC", dataframe['Beg_i (Value) - IMAM Program'], dataframe['beg'])
    dataframe['amar'] = np.where(dataframe['type'] == "SC", dataframe['Amar_i (Value) - IMAM Program'], dataframe['amar'])
    dataframe['tin'] = np.where(dataframe['type'] == "SC", dataframe['Tin_i (Value) - IMAM Program'], dataframe['tin'])
    dataframe['dcur'] = np.where(dataframe['type'] == "SC", dataframe['Dcur_i (Value) - IMAM Program'], dataframe['dcur'])
    dataframe['dead'] = np.where(dataframe['type'] == "SC", dataframe['Dead_i (Value) - IMAM Program'], dataframe['dead'])
    dataframe['defu'] = np.where(dataframe['type'] == "SC", dataframe['DefU_i (Value) - IMAM Program'], dataframe['defu'])
    dataframe['dmed'] = np.where(dataframe['type'] == "SC", dataframe['Dmed_i (Value) - IMAM Program'], dataframe['dmed'])
    dataframe['tout'] = np.where(dataframe['type'] == "SC", dataframe['Tout_i (Value) - IMAM Program'], dataframe['tout'])

    return dataframe