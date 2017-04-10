# functions for data wrangling of imported dataframes.

import pandas as pd
import numpy as np
import time

from isoweek import Week
from datetime import date, timedelta


# CALL THE DATA CLEANING IN LOADING OF EACH DATA SET (PRO, STO, LGA, REG)
# BEFORE LOADING DATA INTO POSTGRES

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
    dataframe.rename(columns={'ProType (Category) - IMAM Program': 'protype'}, inplace=True)
    dataframe.rename(columns={'age group (Category) - IMAM Program': 'age_group'}, inplace=True)
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
    dataframe.rename(columns={'PostLevel (Value) - IMAM Stock': 'level'}, inplace=True)
    dataframe.rename(columns={'WeekNum (Value) - IMAM Stock': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'Self Report (Category) - IMAM Stock': 'self_report'}, inplace=True)
    dataframe.rename(columns={'StoSiteID (Value) - IMAM Stock': 'stositeid'}, inplace=True)
    dataframe.rename(columns={'StoType (Category) - IMAM Stock': 'stotype'}, inplace=True)
    dataframe.rename(columns={'route_by_type (Category) - IMAM Stock': 'type'}, inplace=True)
    dataframe.rename(columns={'RUTF_in (Value) - IMAM Stock': 'rutf_in'}, inplace=True)
    # Outpatients
    dataframe.rename(columns={'RUTF_used_carton (Value) - IMAM Stock': 'rutf_used_carton'}, inplace=True)
    dataframe.rename(columns={'RUTF_used_sachet (Value) - IMAM Stock': 'rutf_used_sachet'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal_carton (Value) - IMAM Stock': 'rutf_bal_carton'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal_sachet (Value) - IMAM Stock': 'rutf_bal_sachet'}, inplace=True)
    # Inpatients
    dataframe.rename(columns={'F75_bal_carton (Value) - IMAM Stock': 'f75_bal_carton'}, inplace=True)
    dataframe.rename(columns={'F75_bal_sachet (Value) - IMAM Stock': 'f75_bal_sachet'}, inplace=True)
    dataframe.rename(columns={'F100_bal_carton (Value) - IMAM Stock': 'f100_bal_carton'}, inplace=True)
    dataframe.rename(columns={'F100_bal_sachet (Value) - IMAM Stock': 'f100_bal_sachet'}, inplace=True)
    # confirm correct data entry
    dataframe.rename(columns={'Confirm (Category) - IMAM Stock': 'confirm'}, inplace=True)

    # LGA database
    dataframe.rename(columns={'WeekNum (Value) - IMAM LGA State Stocks': 'weeknum'}, inplace=True)
    dataframe.rename(columns={'RUTF_in (Value) - IMAM LGA State Stocks': 'rutf_in'}, inplace=True)
    dataframe.rename(columns={'RUTF_out (Value) - IMAM LGA State Stocks': 'rutf_out'}, inplace=True)
    dataframe.rename(columns={'RUTF_bal (Value) - IMAM LGA State Stocks': 'rutf_bal'}, inplace=True)
    dataframe.rename(columns={'Confirm (Category) - IMAM LGA State Stocks': 'confirm'}, inplace=True)
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


def add_program_reports_from_supervision(dataframe):
    # Merge in program reports submitted by supervision staff when implementation staff could not send
    dataframe['siteid'] = np.where(dataframe['role'] != "Site", dataframe['prositeid'], dataframe['siteid'])
    dataframe['type'] = np.where(dataframe['role'] != "Site", dataframe['protype'], dataframe['type'])
    # reports submitted by supervision are identified by role == First or Second
    return dataframe


def add_stock_reports_from_supervision(stock_df):
    # Merge in stock reports submitted by supervision staff when implementation staff could not send
    stock_df['siteid'] = np.where(stock_df['self_report'] == "No", stock_df['stositeid'], stock_df['siteid'])
    stock_df['type'] = np.where(stock_df['self_report'] == "No", stock_df['stotype'], stock_df['type'])
    # reports submitted by supervision are identified by self_report ==  No
    return stock_df


def assign_state_lga_num(dataframe):
    # Set siteid to str to measure length  - only works with strings
    dataframe['siteid_lgt'] = dataframe['siteid'].astype(str).str.len()
    dataframe['state_num'] = dataframe['siteid'].astype(str).str[:2]
    dataframe['lga_num'] = dataframe['siteid'].astype(str).str[:4]

    # Conditional - Numpy - if site id < 10 digits then take first 1 for state or 3 for LGA
    dataframe['state_num'] = np.where(dataframe['siteid_lgt']==9, dataframe['siteid'].astype(str).str[:1], dataframe['state_num'])
    dataframe['lga_num'] = np.where(dataframe['siteid_lgt']==9, dataframe['siteid'].astype(str).str[:3], dataframe['lga_num'])
    return dataframe


    # Follow order for cleaning data for graph
    #  - convert from string to float
    #  - filter out incorrect data with query
    #  - convert from float to int


def generic_cleaning(dataframe):
    # Drop unvalidated data - remember the pandas query has to be in a string.
    dataframe = dataframe.query('confirm=="Yes"')

    # Assign state and LGA numbers to data frame
    dataframe = assign_state_lga_num(dataframe)

    for i in ('weeknum', 'state_num', 'lga_num', 'siteid'):
        # IDs convert from string to float
        dataframe[i] = pd.to_numeric(dataframe[i], errors='coerce')
        # Clean out of range identification data - this deletes entire row where a NaN is found
        dataframe = dataframe.query('%s==%s' % (i, i)).query('%s>=0' % i)
        # Convert from float to int
        dataframe[i] = dataframe[i].astype(int)

    # It is appropriate to delete the entire row of data if there is no ID or week number
    # lines below deletes entire row where a NaN is found - see all queries
    dataframe = dataframe.query('0<weeknum<53')
    dataframe = dataframe.query('0<state_num<37')
    dataframe = dataframe.query('101<lga_num<3799')
    dataframe = dataframe.query('101110001<siteid<3799990999')
    # 2015 had 53 weeks  2016 had 52 weeks
    # Current data is only for weeknumbers from 22-2016 to present
    return dataframe


def add_iso_dates(dataframe):
    # Introducing Year for X axis
    dataframe['year'] = dataframe['last_seen'].map(lambda x: x.year)

    # If report was for WN in last year but report data is this year, subtract one year from dataframe.year.
    # double check if the week number below is ISO standard
    dataframe['last_seen_weeknum'] = dataframe['last_seen'].map(lambda x: x.week)
    dataframe['year'] = np.where(dataframe['last_seen_weeknum'] < dataframe['weeknum'], dataframe['year'] - 1, dataframe['year'])

    # Try loc to identify variable recoding
    #df.loc[:, ['B', 'A']] = df[['A', 'B']].values
    # first input in loc is row, second is column

    today_year = date.today().year
    today_weeknum = date.today().isocalendar()[1]

    # Select Dataframe is includes data from WN22 2016 to 2017+
    # and most recent data cannot surpass current WN and current year.
    dataframe = dataframe \
        [(dataframe['year'] >= 2017) | ((dataframe['year'] == 2016) & (dataframe['weeknum'] >= 22))] \
        [(dataframe['year'] < today_year) | ((dataframe['year'] == today_year) & (dataframe['weeknum'] <= today_weeknum))]

    # Reporting rates
    dataframe['rep_year_wn'] = dataframe['last_seen'].map(lambda x: x.isocalendar())
    # double check if the week number below is ISO standard
    # I don't know the reference for week below, but appears to be ISO week
    dataframe['rep_weeknum'] = dataframe['last_seen'].map(lambda x: x.to_pydatetime().isocalendar()[1])

    # Delete all future reporting -before 10 AM on the first day of the report week.
    dataframe['last_seen_dotw'] = dataframe['last_seen'].map(lambda x: x.to_pydatetime().isocalendar()[2])
    dataframe['last_seen_hour'] = dataframe['last_seen'].map(lambda x: x.to_pydatetime().hour)
    too_early = dataframe.query('last_seen_dotw==1').query('last_seen_hour<10').query('rep_weeknum==weeknum').index.tolist()
    # not dataframe.index isin list of indices too_early
    dataframe = dataframe[~dataframe.index.isin(too_early)]

    dataframe['year_weeknum'] = zip(dataframe['year'], dataframe['weeknum'])
    dataframe['iso_rep_year_wn'] = dataframe['rep_year_wn'].map(lambda x: Week(x[0], x[1]))
    dataframe['iso_year_weeknum'] = dataframe['year_weeknum'].map(lambda x: Week(x[0], x[1]))
    # Remove all reports for dates in the future.
    future_report = dataframe.query('rep_year_wn<year_weeknum').index.tolist()
    dataframe = dataframe[~dataframe.index.isin(future_report)]

    dataframe['iso_diff'] = (dataframe['iso_year_weeknum'] - dataframe['iso_rep_year_wn'])
    # remove reports for 8 weeks prior to report date
    dataframe = dataframe.query('iso_diff>=-8')

    year, week, dotw = date.today().isocalendar()
    current_week = Week(year, week)

    # Report is X weeks before current week number
    dataframe['since_x_weeks'] = dataframe['iso_year_weeknum'].map(lambda x: current_week - x)
    return dataframe


def drop_duplicate_reports(dataframe):
    # CLEAN FUTURE AND DISTANT PAST ENTRIES BEFORE DROPPING DUPLICATES
    # first, reverse sort data by variable last seen
    dataframe = dataframe.sort_values(by='last_seen', ascending=False)
    # second, filter out duplicates - should have one data entry for each siteid by type and weeknum
    dataframe = dataframe.drop_duplicates(['siteid', 'weeknum', 'type'], keep='first')
    return dataframe


def program_cleaning(dataframe):
    for i in ('amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        # data from string to float
        dataframe[i] = pd.to_numeric(dataframe[i], errors='coerce')
        # the change below changes the integrity of data - do not export.
        # This is problematic if the graph shows zero when the data is Null / NaN
        # can you see a zero - look in tooltips
        # no data would be evident from the reporting rate (complete reporting)
        # keep data integrity in postgres db
        dataframe[i] = dataframe[i].fillna(0)
        # Convert from float to int
        dataframe[i] = dataframe[i].astype(int)
    # Data cleaning for admissions
    dataframe = dataframe.query('amar<9999')
    # Make agegroup = 6-59m for all OTPs
    dataframe['age_group'] = np.where(dataframe['type'] == "OTP", "6-59m", dataframe['age_group'])
    return dataframe


def stock_cleaning(dataframe_stock):
    # STOCKS
    dataframe_stock['rutf_bal_carton'] = pd.to_numeric(dataframe_stock.rutf_bal_carton, errors='coerce')
    dataframe_stock['rutf_bal_sachet'] = pd.to_numeric(dataframe_stock.rutf_bal_sachet, errors='coerce')

    dataframe_stock = dataframe_stock.query('rutf_bal_carton==rutf_bal_carton').query('0<=rutf_bal_carton<9999')
    dataframe_stock = dataframe_stock.query('rutf_bal_sachet==rutf_bal_sachet').query('0<=rutf_bal_sachet<9999')

    # Make sure that that this is not needed.  Bad practice to set vars to zero when there was no report.
    # dataframe[i] = dataframe[i].fillna(0)

    dataframe_stock['rutf_bal_carton'] = dataframe_stock.rutf_bal_carton.astype('int')
    dataframe_stock['rutf_bal_sachet'] = dataframe_stock.rutf_bal_sachet.astype('int')

    # add supervision data to main stock data
    return dataframe_stock


def warehouse_cleaning(dataframe):

    return dataframe