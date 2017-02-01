# functions for data wrangling of imported dataframes.

import numpy as np


def create_unique_key(dataframe):
    # Create primary key for program data (phone number and timestamp when report started)
    dataframe['unique'] = dataframe['urn'].astype(str) + " " + dataframe['first_seen'].astype(object).astype(str)


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
    dataframe.rename(columns={'Mail (Value) - IMAM Program ': 'mail'}, inplace=True)
    dataframe.rename(columns={'Post_imp (Value) - IMAM Program ': 'post'}, inplace=True)

    # Program database
    dataframe.rename(columns={'WeekNum (Value) - IMAM *': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'Role (Value) - IMAM *': 'role'}, inplace=True)
    dataframe.rename(columns={'Type (Category) - IMAM *': 'type'}, inplace=True)
    dataframe.rename(columns={'ProSiteID (Value) - IMAM *': 'prositeid'}, inplace=True)
    dataframe.rename(columns={'ProType (Value) - IMAM *': 'protype'}, inplace=True)
    dataframe.rename(columns={'age group (Value) - IMAM *': 'age_group'}, inplace=True)
    # Outpatients admissions and exits
    dataframe.rename(columns={'Beg_o (Value) - IMAM *': 'beg'}, inplace=True)
    dataframe.rename(columns={'Amar_o (Value) - IMAM *': 'amar'}, inplace=True)
    dataframe.rename(columns={'Tin_o (Value) - IMAM *': 'tin'}, inplace=True)
    dataframe.rename(columns={'Dcur_o (Value) - IMAM *': 'dcur'}, inplace=True)
    dataframe.rename(columns={'Dead_o (Value) - IMAM *': 'dead'}, inplace=True)
    dataframe.rename(columns={'DefU_o (Value) - IMAM *': 'defu'}, inplace=True)
    dataframe.rename(columns={'Dmed_o (Value) - IMAM *': 'dmed'}, inplace=True)
    dataframe.rename(columns={'Tout_o (Value) - IMAM *': 'tout'}, inplace=True)
    # confirm correct data entry
    dataframe.rename(columns={'Confirm (Category) - IMAM *': 'confirm'}, inplace=True)
    # old var name
    dataframe.rename(columns={'confirm (Category) - IMAM *': 'confirm'}, inplace=True)

    # Stock database
    dataframe.rename(columns={'Self Report (Value) - IMAM * ': 'self_report'}, inplace=True)
    dataframe.rename(columns={'StoSiteID (Value) - IMAM * ': 'sto_siteid'}, inplace=True)
    dataframe.rename(columns={'StoType (Category) - IMAM * ': 'sto_type'}, inplace=True)
    dataframe.rename(columns={'route_by_type (Category) - IMAM * ': 'type'}, inplace=True)
    dataframe.rename(columns={'RUTF_in (Value) - IMAM *': 'rutf_in'}, inplace=True)
    # Outpatients
    dataframe.rename(columns={'RUTF_used_carton (Value) - IMAM *': 'rutf_used_carton'}, inplace=True)
    dataframe.rename(columns={'RUTF_used_sachet (Value) - IMAM *': 'rutf_used_sachet'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal_carton (Value) - IMAM *': 'rutf_bal_carton'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal_sachet (Value) - IMAM *': 'rutf_bal_sachet'}, inplace=True)
    # Inpatients
    dataframe.rename(columns={'F75_bal_carton (Value) *': 'f75_bal_carton'}, inplace=True)
    dataframe.rename(columns={'F75_bal_sachet (Value) *': 'f75_bal_sachet'}, inplace=True)
    dataframe.rename(columns={'F100_bal_carton (Value) *': 'f100_bal_carton'}, inplace=True)
    dataframe.rename(columns={'F100_bal_sachet (Value) *': 'f100_bal_sachet'}, inplace=True)
    # LGA database
    dataframe.rename(columns={'RUTF_out (Value) - IMAM *': 'rutf_out'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal (Value) - IMAM *': 'rutf_bal'}, inplace=True)
    # do not need stock alert variables as they are based on actual stocks

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


def assign_state_lga_num(dataframe):
    # Set siteid to str to measure length  - only works with strings
    dataframe['siteid_lgt'] = dataframe['siteid'].astype(str).str.len()
    dataframe['state_num'] = dataframe['siteid'].astype(str).str[:2]
    dataframe['state_num'] = np.where(dataframe['siteid_lgt']==9, dataframe['siteid'].astype(str).str[:1], dataframe['state_num'])
    dataframe['lga_num'] = dataframe['siteid'].astype(str).str[:4]
    dataframe['lga_num'] = np.where(dataframe['siteid_lgt']==9, dataframe['siteid'].astype(str).str[:3], dataframe['lga_num'])

    return dataframe
