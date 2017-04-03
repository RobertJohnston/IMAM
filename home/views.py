import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import time
import numpy as np
from isoweek import Week

from datetime import date, timedelta
from sqlalchemy import create_engine
from management.commands.load_data import assign_state_lga_num

from models import First_admin, Second_admin, Site


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta

# There is an error with this as week 52 of 2016 is presented as 2017 (first week of year)
# This appears to be a highcharts presentation problem and not an error
def iso_to_gregorian(iso_year, iso_week, iso_day=1):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return int((year_start + timedelta(days=iso_day - 1, weeks=iso_week - 1)).strftime('%s') + '000')


def data_cleaning_and_preparation(df, df_stock):
    # CLEAN FUTURE AND DISTANT PAST ENTRIES BEFORE DROPPING DUPLICATES



    # Assign state and LGA numbers to data frame
    df = assign_state_lga_num(df)

    # Follow order for cleaning data for graph
    #  - convert from string to float
    #  - filter out incorrect data with query
    #  - convert from float to int

    # Convert from string to float
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid', 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df[i] = pd.to_numeric(df[i], errors='coerce')

    # Clean out of range identification data
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid'):
        df = df.query('%s==%s' % (i, i)).query('%s>=0' % i)
        # line above deletes entire row where a NaN is found

    # the change below changes the integrity of data - do not export.
    # This is problematic if the graph shows zero when the data is Null / NaN
    # can you see a zero - look in tooltips
    # no data would be evident from the reporting rate (complete reporting)
    # keep data integrity in postgres db - change Null to zero in working df
    for i in ( 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df[i] = df[i].fillna(0)


    # It is appropriate to delete the entire row of data if there is no ID or week number
    # lines below deletes entire row where a NaN is found - see all queries
    df = df.query('0<weeknum<53')
    df = df.query('0<state_num<37')
    df = df.query('101<lga_num<3799')
    df = df.query('101110001<siteid<3799999999')

    # Data cleaning for admissions
    df = df.query('amar<99999')

    # Convert from float to int
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid', 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df[i] = df[i].astype(int)


    # Introducing Year for X axis
    df['year'] = df['last_seen'].map(lambda x: x.year)

    # double check if the week number below is ISO standard
    df['last_seen_weeknum'] = df['last_seen'].map(lambda x: x.week)

    df['year'] = np.where(df['last_seen_weeknum'] < df['weeknum'],
                                        df['year'] - 1, df['year'])

    today_year = date.today().year
    today_weeknum = date.today().isocalendar()[1]

    # df = df.sort_values(['year', 'weeknum'])
    df = df\
        [(df['year'] >= 2017) | ((df['year'] == 2016) & (df['weeknum'] >= 22))]\
        [(df['year'] < today_year) | ((df['year'] == today_year) & (df['weeknum'] <= today_weeknum))]


    # Reporting rates
    df['rep_year_wn'] = df['last_seen'].map(lambda x: x.isocalendar())
    # double check if the week number below is ISO standard
    # I don't know the reference for week below, but appears to be ISO week
    df['rep_weeknum'] = df['last_seen'].map(lambda x: x.to_pydatetime().isocalendar()[1])

    # delete all future reporting -before 10 am on the first day of the report week.
    df['last_seen_dotw'] = df['last_seen'].map(lambda x: x.to_pydatetime().isocalendar()[2])
    df['last_seen_hour'] = df['last_seen'].map(lambda x: x.to_pydatetime().hour)
    # df.query('last_seen_dotw==1').query('last_seen_hour<10').query('rep_weeknum==weeknum')['name'].groupby(df['name']).count().plot(kind='bar', rot=90)
    too_early = df.query('last_seen_dotw==1').query('last_seen_hour<10').query('rep_weeknum==weeknum').index.tolist()
    df = df[~df.index.isin(too_early)]

    df['year_weeknum'] = zip(df['year'], df['weeknum'])
    df['iso_rep_year_wn'] = df['rep_year_wn'].map(lambda x: Week(x[0], x[1]))
    df['iso_year_weeknum'] = df['year_weeknum'].map(lambda x: Week(x[0], x[1]))
    # Remove all reports for dates in the future.
    future_report = df.query('rep_year_wn<year_weeknum').index.tolist()
    df = df[~df.index.isin(future_report)]

    df['iso_diff'] = (df['iso_year_weeknum'] - df['iso_rep_year_wn'])
    # remove reports for 8 weeks prior to report date
    df = df.query('iso_diff>=-8')

    year, week, dotw = date.today().isocalendar()
    current_week = Week(year, week)

    # since how many week this report is about
    df['since_x_weeks'] = df['iso_year_weeknum'].map(lambda x: current_week - x)

    # Drop duplicates from database
    # first, reverse sort data by variable last seen
    df = df.sort_values(by='last_seen', ascending=False)
    # second, filter out duplicates - should have one data entry for each siteid by type and weeknum
    df = df.drop_duplicates(['siteid', 'weeknum', 'type'], keep='first')

    df_stock['siteid'] = pd.to_numeric(df_stock.siteid, errors='coerce')
    df_stock['weeknum'] = pd.to_numeric(df_stock.weeknum, errors='coerce')
    df_stock['rutf_bal_carton'] = pd.to_numeric(df_stock.rutf_bal_carton, errors='coerce')
    df_stock['rutf_bal_sachet'] = pd.to_numeric(df_stock.rutf_bal_sachet, errors='coerce')

    df_stock = df_stock.query('siteid==siteid').query('0<siteid<3999990999')
    # 2015 had 53 weeks
    # 2016 had 52 weeks - current data is only for weeknumbers from 22-2016 to present
    df_stock = df_stock.query('weeknum==weeknum').query('0.99<weeknum<53')
    df_stock = df_stock.query('rutf_bal_carton==rutf_bal_carton').query('0<=rutf_bal_carton<9999')
    df_stock = df_stock.query('rutf_bal_sachet==rutf_bal_sachet').query('0<=rutf_bal_sachet<9999')

    df_stock['siteid'] = df_stock.siteid.astype('int')
    df_stock['weeknum'] = df_stock.weeknum.astype('int')
    df_stock['rutf_bal_carton'] = df_stock.rutf_bal_carton.astype('int')
    df_stock['rutf_bal_sachet'] = df_stock.rutf_bal_sachet.astype('int')

    # Drop unvalidated data
    df_stock = df_stock.query('confirm=="Yes"')
    # Before filter - Sort data
    df_stock = df_stock.sort_values(by='last_seen', ascending=False)
    df_stock = df_stock.drop_duplicates(['siteid', 'weeknum', 'type'], keep='first')

    df_stock['year'] = df_stock['last_seen'].map(lambda x: x.year)
    df_stock['last_seen_weeknum'] = df_stock['last_seen'].map(lambda x: x.week)
    df_stock['year'] = np.where(df_stock['last_seen_weeknum'] < df_stock['weeknum'],
                          df_stock['year'] - 1, df_stock['year'])

    
    return df, df_stock


def rate_by_week(df_filtered, df_stock, kind=None, num=None):
    # this is national level, no need for query
    if kind is None:
        df_queried = df_filtered

    else:
        df_queried = df_filtered.query('%s==%s' % (kind, num))

    report_rate = df_queried.query('since_x_weeks<=8').groupby(df_queried['siteid'])[
        'weeknum'].count().map(lambda x: (x / 8.) * 100).mean()


    if kind == 'siteid':
        latest_stock_report = df_stock.query('year==2017').query('siteid==%s' % num).sort_values(by='weeknum', ascending=False).drop_duplicates(
            ['siteid'], keep='first')['rutf_bal_carton'].tolist()

        latest_stock_report = latest_stock_report[0] if len(latest_stock_report) != 0 else None

        latest_stock_report_weeknum = df_stock.query('year==2017').query('siteid==%s' % num).sort_values(by='weeknum', ascending=False).drop_duplicates(
            ['siteid'], keep='first')['weeknum'].tolist()

        latest_stock_report_weeknum = latest_stock_report_weeknum[0] if len(latest_stock_report_weeknum) != 0 else None

    # for National, State, and LGA level
    else:
        latest_stock_report = None
        latest_stock_report_weeknum = None

    print(kind, latest_stock_report, latest_stock_report_weeknum)

    adm_by_week = df_queried['amar'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum()

    # filter by one site
    # percentage of complete reporting for one site
    # ATTENTION
    # denominator is the number of sites that have at least one person registered with IMAM program

    filter_discharge = df_queried['total_discharges'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum()
    filter_cout = df_queried['cout'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum()

    # Was year added into groupby here ?
    dead_rate_by_week = df_queried['dead'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_discharge * 100
    defu_rate_by_week = df_queried['defu'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_discharge * 100
    dmed_rate_by_week = df_queried['dmed'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_discharge * 100
    tout_rate_by_week = df_queried['tout'].groupby([df_filtered['year'], df_filtered['weeknum']]).sum() / filter_cout * 100

    dead_rate_by_week = dead_rate_by_week.dropna()
    defu_rate_by_week = defu_rate_by_week.dropna()
    dmed_rate_by_week = dmed_rate_by_week.dropna()
    tout_rate_by_week = tout_rate_by_week.dropna()
    
    return adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week, report_rate, latest_stock_report, latest_stock_report_weeknum


# Query database and create data for admissions graph
def adm(request):
    # Read data into dataframe - at each function call
    engine = create_engine(
        'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
    df = pd.read_sql_query("select * from program;", con=engine)
    df_stock = pd.read_sql_query("select * from stock;", con=engine)

    # All data should be cleaned in advance.
    df_filtered, df_stock = data_cleaning_and_preparation(df, df_stock)

    # For all exit rate calculations see Final Report Consensus Meeting on M&E IMAM December 2010
    # UNICEF WCARO - Dakar Senegal

    # Filter by Year
    df_filtered = df_filtered.query("year==%s" % request.GET.get("year", "2017"))

    # Filter by Site Type (all, outpatients OTP, inpatients IPF or SC)
        # There is no data in type var of ALL only OTP and SC

    if "site_type" not in request.GET or request.GET['site_type'] == "All" or request.GET['site_type'] not in ("OTP", "SC"):
        df_filtered = df_filtered
    elif request.GET['site_type'] == "OTP":
        df_filtered = df_filtered.query('type=="OTP"')
        # if var name type == string - must be within quotes
    elif request.GET['site_type'] == "SC":
        df_filtered = df_filtered.query('type=="SC"')
    else:
        raise Exception("This site_type value is not permitted: %s" % request.GET['site_type'])

    # Total Discharges from program
    df_filtered['total_discharges'] = df_filtered.dcur + df_filtered.dead + df_filtered.defu + df_filtered.dmed

    # Total Exits from implementation site - Cout (Mike Golden term) includes the internal transfers - tout
    df_filtered['cout'] = df_filtered.total_discharges + df_filtered.tout



    result = {}

    # default or national level
    if "site_filter" not in request.GET or request.GET['site_filter'] in ("", "null"):
        adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week, report_rate, latest_stock_report, latest_stock_report_weeknum = rate_by_week(df_filtered, df_stock)

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
            adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week, report_rate , latest_stock_report, latest_stock_report_weeknum= rate_by_week(df_filtered, df_stock, kind, num)

            # in line below, django expects only one = to get value.
            first_admin = First_admin.objects.get(state_num=num)

            title = "%s %s" % (first_admin.state, data_type.capitalize())

        elif data_type == "lga":
            kind = "lga_num"
            adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week, report_rate, latest_stock_report, latest_stock_report_weeknum = rate_by_week(df_filtered, df_stock, kind, num)

            second_admin = Second_admin.objects.get(lga_num=num)
            title = "%s-LGA %s" % (second_admin.lga.title(),
                                   second_admin.state_num.state.title())

        elif data_type == "site":
            # result = rate_by_week(result, df_filtered, 'siteid')
            kind = "siteid"
            adm_by_week, dead_rate_by_week, defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week, report_rate, latest_stock_report, latest_stock_report_weeknum = rate_by_week(df_filtered, df_stock, kind, num)

            site_level = Site.objects.get(siteid=num)
            title = "%s,  %s-LGA %s " % (site_level.sitename.title(),
                                         site_level.lga_num.lga.title(),
                                         site_level.state_num.state)

        else:
            raise Exception("We have encountered a datatype that we don't know how to handle: %s" % data_type)

    adm_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in adm_by_week.index], adm_by_week.values.tolist()))

    dead_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in dead_rate_by_week.index], dead_rate_by_week.values.tolist()))
    defu_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in defu_rate_by_week.index], defu_rate_by_week.values.tolist()))
    dmed_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in dmed_rate_by_week.index], dmed_rate_by_week.values.tolist()))
    tout_rate_by_week = list(zip([iso_to_gregorian(x[0], x[1]) for x in tout_rate_by_week.index], tout_rate_by_week.values.tolist()))

    # return HttpResponse(json.dumps(result)
    return HttpResponse(json.dumps({
        "adm_by_week": adm_by_week,
        "dead_rate_by_week": dead_rate_by_week,
        "defu_rate_by_week": defu_rate_by_week,
        "dmed_rate_by_week": dmed_rate_by_week,
        "tout_rate_by_week": tout_rate_by_week,
        "latest_stock_report": latest_stock_report,
        "latest_stock_report_weeknum": latest_stock_report_weeknum,
        "report_rate": "%2.1f" % report_rate,
        "title": title,
        "date": date.today().strftime("%d-%m-%Y"),
    }))




def index(request):
    state_list = First_admin.objects.all().order_by('state_num')

    lga_list = Second_admin.objects.all().order_by('lga_num')

    site_list = Site.objects.all().order_by('siteid')

    return render(request, 'home/index.html', {"state_list": state_list,
                                               "lga_list": lga_list,
                                               "site_list": site_list,
                                               })


# filling select2 options - Query to fill options in select box
def search(request):
    result = []
    total_count = 0
    page_number = int(request.GET['page']) if 'page' in request.GET else 1

    if 'q' in request.GET:
        ajax_query = request.GET['q']

        # the real total count should be the addition of the count of states, lga and sites
        total_count = Site.objects.filter(sitename__icontains=ajax_query).count()

        if page_number == 1 and ajax_query.lower() in "National".lower():
            result = [
                {"id": "", "text": "National"},
            ]

        for state in First_admin.objects.filter(state__icontains=ajax_query)[20 * (page_number - 1):20 * page_number]:
            result.append({"id": "state-%s" % state.state_num, "text": state.state.title()})

        for lga in Second_admin.objects.filter(lga__icontains=ajax_query)[20 * (page_number - 1):20 * page_number]:
            result.append({"id": "lga-%s" % lga.lga_num, "text": "%s LGA" % lga.lga})

        for i in Site.objects.filter(sitename__icontains=ajax_query)[20 * (page_number - 1):20 * page_number]:
            # double underscore Django convention
            # https://docs.djangoproject.com/en/1.10/topics/db/queries/#field-lookups

            # Select2 wants the data in this format
            # var data = [{id: 0, text: 'enhancement'}, ];

            # ADD STATE

            # ADD LGA

            # value="site-{{ site.siteid }}">{{ site.sitename }}
            result.append({"id": "site-%s" % i.siteid, "text": i.sitename})

    else:
        total_count = Site.objects.all().count()

        if page_number == 1:
            result = [
                {"id": "", "text": "National"},
            ]

            for state in First_admin.objects.all():
                result.append({"id": "state-%s" % state.state_num, "text": state.state})

        for lga in Second_admin.objects.all()[20 * (page_number - 1):20 * page_number]:
            result.append({"id": "lga-%s" % lga.lga_num, "text": "%s LGA" % lga.lga})

        for i in Site.objects.all()[20 * (page_number - 1):20 * page_number]:
            result.append({"id": "site-%s" % i.siteid, "text": i.sitename})

    return HttpResponse(json.dumps({
        "items": result,
        "total_count": total_count,
    }))