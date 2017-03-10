import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import time
import numpy as np

from datetime import date, timedelta

from sqlalchemy import create_engine
from management.commands.load_data import assign_state_lga_num

from models import First_admin, Second_admin, Site


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day=1):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return int((year_start + timedelta(days=iso_day - 1, weeks=iso_week - 1)).strftime('%s') + '000')


def rate_by_week(df_filtered, kind=None, num=None):
    # this is nationnal level, no need for query
    if kind is None:
        df_queried = df_filtered
    else:
        df_queried = df_filtered.query('%s==%s' % (kind, num))

    adm_by_week = df_queried['amar'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum()

    filter_discharge = df_queried['total_discharges'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum()
    filter_cout = df_queried['cout'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum()

    dead_rate_by_week = df_queried['dead'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_discharge * 100
    defu_rate_by_week = df_queried['defu'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_discharge * 100
    dmed_rate_by_week = df_queried['dmed'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_discharge * 100
    tout_rate_by_week = df_queried['tout'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_cout * 100

    dead_rate_by_week = dead_rate_by_week.dropna()
    defu_rate_by_week = defu_rate_by_week.dropna()
    dmed_rate_by_week = dmed_rate_by_week.dropna()
    tout_rate_by_week = tout_rate_by_week.dropna()
    
    return adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week


# Query database and create data for admissions graph
def adm(request):
    # Read data into dataframe - at each function call
    engine = create_engine(
        'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
    df = pd.read_sql_query("select * from program;", con=engine)

    # All data should be cleaned in advance.

    # Remove duplicates from database
    # Reverse sort data by last seen
    df = df.sort_values(by='last_seen', ascending=False)
    # Filter out duplicates - should have one data entry for each siteid by type and weeknum
    df_filtered = df.drop_duplicates(['siteid', 'weeknum', 'type'], keep='first')

    # Assign state and LGA numbers to data frame
    df_filtered = assign_state_lga_num(df_filtered)

    # Follow following order for cleaning data for graph
    #  - convert from string to float
    #  - filter out incorrect data with query
    #  - convert from float to int

    # Convert from string to float
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid', 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df_filtered[i] = pd.to_numeric(df_filtered[i], errors='coerce')

    # Clean out of range identification data
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid'):
        df_filtered = df_filtered.query('%s==%s' % (i, i)).query('%s>=0' % i)
        # line above deletes entire row where a NaN is found

    # the change below changes the integrity of data - do not export.
    for i in ( 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df_filtered[i] = df_filtered[i].fillna(0)


    # It is appropriate to delete the entire row of data if there is no ID or week number
    # line below deletes entire row where a NaN is found - see all queries
    df_filtered = df_filtered.query('0<weeknum<53')
    df_filtered = df_filtered.query('0<state_num<37')
    df_filtered = df_filtered.query('101<lga_num<3799')
    df_filtered = df_filtered.query('101110001<siteid<3799999999')

    # Data cleaning for admissions
    df_filtered = df_filtered.query('amar<99999')

    # Convert from float to int
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid', 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df_filtered[i] = df_filtered[i].astype(int)

    # Introducing Year for X axis
    df_filtered['year'] = df_filtered['last_seen'].map(lambda x: x.year)
    # double check if the week number below is ISO standard
    df_filtered['last_seen_weeknum'] = df_filtered['last_seen'].map(lambda x: x.week)

    df_filtered['year'] = np.where(df_filtered['last_seen_weeknum'] < df_filtered['weeknum'],
                                        df_filtered['year'] - 1, df_filtered['year'])

    today_year = date.today().year
    today_weeknum = date.today().isocalendar()[1]

    # df_filtered = df_filtered.sort_values(['year', 'weeknum'])\
    df_filtered = df_filtered\
        [(df_filtered['year'] >= 2017) | ((df_filtered['year'] == 2016) & (df_filtered['weeknum'] >= 22))]\
        [(df_filtered['year'] < today_year) | ((df_filtered['year'] == today_year) & (df_filtered['weeknum'] <= today_weeknum))]

    # For all exit rate calculations see Final Report Consensus Meeting on M&E IMAM December 2010

    # Total Discharges from program
    df_filtered['total_discharges'] = df_filtered.dcur + df_filtered.dead + df_filtered.defu + df_filtered.dmed

    # Total Exits from implementation site - Cout (Mike Golden term) includes the internal transfers - tout
    df_filtered['cout'] = df_filtered.total_discharges + df_filtered.tout

    result = {}

    # default or national level
    if "site_filter" not in request.GET or request.GET['site_filter'] == "":
        adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()

        adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week = rate_by_week(df_filtered)

        title = "National Level"

    else:
        # request format is: state-23, lga-333, siteid-101110001
        # Last input on split ", 1)"  only allows one split on request.GET to protect against dangerous user input
        data_type, num = request.GET['site_filter'].split('-', 1)
        # add name to datatype here

        # Always sanitize input for security
        # ideally we should use a django form here
        assert num.isdigit()

        if data_type == "state":
            kind = "state_num"
            adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week = rate_by_week(df_filtered, kind, num)

            # in line below, django expects only one = to get value.
            first_admin = First_admin.objects.get(state_num=num)

            title = "%s %s" % (first_admin.state, data_type.capitalize())

        elif data_type == "lga":
            kind = "lga_num"
            adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week = rate_by_week(df_filtered, kind, num)

            second_admin = Second_admin.objects.get(lga_num=num)
            title = "%s-LGA %s" % (second_admin.lga.title(),
                                   second_admin.state_num.state.title())

        elif data_type == "site":
            # result = rate_by_week(result, df_filtered, 'siteid')
            kind = "siteid"
            adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week = rate_by_week(df_filtered, kind, num)

            site_level = Site.objects.get(siteid=num)
            title = "%s,  %s-LGA %s " % (site_level.sitename.title(),
                                        site_level.lga_num.lga.title(),
                                        site_level.state_num.state.title())

        else:
            raise Exception("We have encountered a datatype that we don't know how to handle: %s" % data_type)

    adm_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in adm_by_week.index], adm_by_week.values.tolist()))

    dead_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in dead_rate_by_week.index], dead_rate_by_week.values.tolist()))
    defu_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in defu_rate_by_week.index], defu_rate_by_week.values.tolist()))
    dmed_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in dmed_rate_by_week.index], dmed_rate_by_week.values.tolist()))
    tout_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in tout_rate_by_week.index], tout_rate_by_week.values.tolist()))

    # date = {'date': time.strftime("%d/%m/%y")}

    # return HttpResponse(json.dumps(result)

    return HttpResponse(json.dumps({
        "adm_by_week": adm_by_week,
        "dead_rate_by_week": dead_rate_by_week,
        "defu_rate_by_week": defu_rate_by_week,
        "dmed_rate_by_week": dmed_rate_by_week,
        "tout_rate_by_week": tout_rate_by_week,
        "title": title,
        "date": date.today().strftime("%d/%m/%Y"),
        #   Cannot pass data through because of json dumps?
    }))




def index(request):
    state_list = First_admin.objects.all().order_by('state_num')

    lga_list = Second_admin.objects.all().order_by('lga_num')

    site_list = Site.objects.all().order_by('siteid')

    return render(request, 'home/index.html', {"state_list": state_list,
                                               "lga_list": lga_list,
                                               "site_list": site_list,
                                               })





