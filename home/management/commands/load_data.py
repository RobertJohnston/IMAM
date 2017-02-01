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
    dataframe.rename(columns={'Type (Value) - IMAM Program': 'type'}, inplace=True)
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
    dataframe.rename(columns={'PostLevel (Value) - IMAM Stock ': 'level'}, inplace=True)
    dataframe.rename(columns={'WeekNum (Value) - IMAM Stock ': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'Self Report (Value) - IMAM Stock ': 'self_report'}, inplace=True)
    dataframe.rename(columns={'StoSiteID (Value) - IMAM Stock ': 'sto_siteid'}, inplace=True)
    dataframe.rename(columns={'StoType (Category) - IMAM Stock ': 'sto_type'}, inplace=True)
    dataframe.rename(columns={'route_by_type (Category) - IMAM Stock ': 'type'}, inplace=True)
    dataframe.rename(columns={'RUTF_in (Value) - IMAM Stock ': 'rutf_in'}, inplace=True)
    # Outpatients
    dataframe.rename(columns={'RUTF_used_carton (Value) - IMAM Stock ': 'rutf_used_carton'}, inplace=True)
    dataframe.rename(columns={'RUTF_used_sachet (Value) - IMAM Stock ': 'rutf_used_sachet'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal_carton (Value) - IMAM Stock ': 'rutf_bal_carton'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal_sachet (Value) - IMAM Stock ': 'rutf_bal_sachet'}, inplace=True)
    # Inpatients
    dataframe.rename(columns={'F75_bal_carton (Value) - IMAM Stock ': 'f75_bal_carton'}, inplace=True)
    dataframe.rename(columns={'F75_bal_sachet (Value) - IMAM Stock ': 'f75_bal_sachet'}, inplace=True)
    dataframe.rename(columns={'F100_bal_carton (Value) - IMAM Stock ': 'f100_bal_carton'}, inplace=True)
    dataframe.rename(columns={'F100_bal_sachet (Value) - IMAM Stock ': 'f100_bal_sachet'}, inplace=True)
    # confirm correct data entry
    dataframe.rename(columns={'Confirm (Category) - IMAM Stock ': 'confirm'}, inplace=True)

    # LGA database
    dataframe.rename(columns={'WeekNum (Value) - IMAM LGA State Stocks': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'RUTF_in (Value) - IMAM LGA State Stocks': 'rutf_in'}, inplace=True)
    dataframe.rename(columns={'RUTF_out (Value) - IMAM LGA State Stocks': 'rutf_out'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal (Value) - IMAM LGA State Stocks': 'rutf_bal'}, inplace=True)
    dataframe.rename(columns={'confirm (Category) - IMAM LGA State Stocks': 'confirm'}, inplace=True)

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