import json
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import numpy as np

from isoweek import Week

from datetime import date, timedelta
from sqlalchemy import create_engine
# We can replace sqlalchemy for django at some point.

from models import First_admin, Second_admin, Site
from utilities import iso_year_start, iso_to_gregorian, weeks_for_year

def json_for_charts(year, site_level, siteid, site_type):
    # Read data into dataframe - at each function call
    engine = create_engine(
        'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
    # PROGRAM DATA
    df = pd.read_sql_query("select * from program;", con=engine)
    # STOCK DATA
    df_stock = pd.read_sql_query("select * from stock;", con=engine)

    # REMOVE THIS WHEN DATA CLEANING IS DONE.
    # F75 sachets per carton - 120
    df_stock['f75_bal'] = df_stock['f75_bal_carton'] + (df_stock['f75_bal_sachet'] / 120.)
    # F100 sachets per carton - 90
    df_stock['f100_bal'] = df_stock['f100_bal_carton'] + (df_stock['f100_bal_sachet'] / 90.)

    # WAREHOUSE DATA
    df_warehouse = pd.read_sql_query("select * from warehouse;", con=engine)

    df_filtered = df
    df_stock_filtered = df_stock
    df_warehouse_filtered = df_warehouse

    current_year, current_week, _ = date.today().isocalendar()

    # For all exit rate calculations see Final Report Consensus Meeting on M&E IMAM December 2010
    # UNICEF WCARO - Dakar Senegal

    # Filter by Year
    df_filtered = df_filtered.query("year==%s" % year)
    df_stock_filtered = df_stock_filtered.query("year==%s" % year)
    df_warehouse_filtered = df_warehouse_filtered.query("year==%s" % year)

    # Filter by Site Type (all, outpatients OTP, inpatients IPF or SC)
    if site_type == "All":
        df_filtered = df_filtered
        df_stock_filtered = df_stock_filtered
    elif site_type == "OTP":
        df_filtered = df_filtered.query('type=="OTP"')
        df_stock_filtered = df_stock_filtered.query('type=="OTP"')
        # if var name type == string - must be within quotes
    elif site_type == "SC":
        df_filtered = df_filtered.query('type=="SC"')
        df_stock_filtered = df_stock_filtered.query('type=="SC"')
    else:
        raise Exception("This site_type value is not permitted: %s" % site_type)

    # Total Discharges from program
    df_filtered['total_discharges'] = df_filtered.dcur + df_filtered.dead + df_filtered.defu + df_filtered.dmed

    # Total Exits from implementation site - Cout (Mike Golden term) includes the internal transfers - Tout
    df_filtered['cout'] = df_filtered.total_discharges + df_filtered.tout


    # default or national level
    if site_level == "National":
        number_of_inactive_sites, number_of_active_sites, adm_by_week, dead_rate_by_week,\
        defu_rate_by_week, dmed_rate_by_week, tout_rate_by_week, program_report_rate, stock_report_rate,\
        stock_by_week, two_weeks_margin = rate_by_week(df_filtered, df_stock_filtered, df_warehouse_filtered)

        title = "National Level"

        # list of most recent stock reports from states
        state_df = df_warehouse_filtered.sort_values(by=['year', 'weeknum'], ascending=[0, 0]).drop_duplicates(subset='siteid')
        state_df = state_df.query('siteid<40').query('siteid>1')
        all_states = pd.read_sql_query("select * from first_admin;", con=engine)
        merge_states = pd.merge(left=all_states, right=state_df, left_on='state_num', right_on='siteid', how='outer')

        recent_stock_report = []
        for index, row in merge_states.iterrows():
            recent_stock_report.append({
                "site": row['state'],
                "siteid": row['state_num'],
                "kind": "state",
                "weeknum": int(row['weeknum']) if row['weeknum'] == row['weeknum'] else False,
                "year": int(row['year']) if row['year'] == row['year'] else "",
                "balance": "{:,}".format(int(row['rutf_bal'])) if row['rutf_bal'] == row['rutf_bal'] else "No Data"
            })

    else:
        data_type, num = site_level, siteid
        # add name to datatype here

        # Always sanitize input for security
        # ideally we should use a django form here
        assert num.isdigit()

        # stock reports for state, lga and site
        recent_stock_report = []

        if data_type == "state":
            kind = "state_num"
            number_of_inactive_sites, number_of_active_sites, adm_by_week, dead_rate_by_week, defu_rate_by_week,\
            dmed_rate_by_week, tout_rate_by_week, program_report_rate, stock_report_rate,\
            stock_by_week, two_weeks_margin = rate_by_week(df_filtered, df_stock_filtered, df_warehouse_filtered, kind, num)

            # in line below, django expects only one equal sign to compare value.
            first_admin = First_admin.objects.get(state_num=num)
            title = "%s %s" % (first_admin.state, data_type.capitalize())

            # Most recent stock reports
            lga_df = df_warehouse_filtered.sort_values(by=['year', 'weeknum'], ascending=[0,0]).drop_duplicates(subset='siteid')
            # FIXME do data cleaning remove future reports
            # Double check that all future reporting is removed in data cleaning
            all_program_lgas = pd.read_sql_query("select * from registration;", con=engine)
            lga_num_min = all_program_lgas['lga_num'].min(axis=0)  # min and max of lga num are used to clean data
            lga_num_max = all_program_lgas['lga_num'].max(axis=0)
            all_program_lgas = all_program_lgas.query('state_num==%s & siteid>=@lga_num_min & siteid<=@lga_num_max' % num)
            all_program_lgas = all_program_lgas.sort_values(by=['lga_num', 'siteid'], ascending=[1, 1])\
                .drop_duplicates(subset='lga_num')
            merge_lga = pd.merge(left=all_program_lgas, right=lga_df, left_on='lga_num', right_on='siteid',
                                 how='outer', sort = False)
            merge_lga['lga_num'] = pd.to_numeric(merge_lga['lga_num'], errors='coerce')
            merge_lga = merge_lga.query('lga_num==lga_num') # remove all cases of NaN
            merge_lga['lga_num'] = merge_lga['lga_num'].astype('int')
            # Add site name from postgres
            merge_lga.loc[:, 'lga'] = merge_lga['lga_num'].map(lambda x: Second_admin.objects.get(lga_num=x)
                    .lga.strip() + " LGA" if Second_admin.objects.filter(lga_num=x) else "")
            # Query one state - query is completed above on the registration date - so all sites are included
            # merge_lga = merge_lga.query('state_num==%s' % num)

            for index, row in merge_lga.iterrows():
                recent_stock_report.append({
                    "site": row['lga'],
                    "siteid": row['lga_num'],
                    "kind": "lga",
                    "weeknum": int(row['weeknum']) if row['weeknum'] == row['weeknum'] else False,
                    "year": int(row['year']) if row['year'] == row['year'] else "",
                    "balance": "{:,}".format(int(row['rutf_bal'])) if row['rutf_bal'] == row['rutf_bal'] else "No Data"
                })

        elif data_type == "lga":
            kind = "lga_num"
            number_of_inactive_sites, number_of_active_sites, adm_by_week, dead_rate_by_week, defu_rate_by_week,\
            dmed_rate_by_week, tout_rate_by_week, program_report_rate, stock_report_rate,\
            stock_by_week, two_weeks_margin = rate_by_week(df_filtered, df_stock_filtered, df_warehouse_filtered, kind, num)

            second_admin = Second_admin.objects.get(lga_num=num)
            title = "%s-LGA %s" % (second_admin.lga.title(),
                                   second_admin.state_num.state.title())

            # Most recent stock report - LGA
            # select one LGA
            site_df = df_stock_filtered.query('lga_num==%s' % num)

            # FIXME don't hardcode week number and do data cleaning instead in the future
            site_df = site_df.query('siteid>201000000').query('year >= 2017 | (weeknum < 22 & year == 2016)')

            # FIXME Must add in most recent reports for stabilization centers also
            site_df = site_df.query('type=="OTP"')

            site_df = site_df.sort_values(by=['year', 'weeknum', 'type'], ascending=[0, 0, 0])
            site_df = site_df.drop_duplicates(subset=['siteid', 'type'])
            # Add site name from postgres
            site_df.loc[:, 'sitename'] = site_df['siteid'].map(lambda x: Site.objects.get(siteid=x)
                                    .sitename.strip() if Site.objects.filter(siteid=x) else "")

            for index, row in site_df.iterrows():
                recent_stock_report.append({
                    "site": row['sitename'],
                    "siteid": row['siteid'],
                    "kind": "site",
                    "weeknum": int(row['weeknum']) if row['weeknum'] == row['weeknum'] else False,
                    # try to add backslash to weeknum so that presentation on recent stock report is correct
                    "year": int(row['year']) if row['year'] == row['year'] else "",
                    # try to add year to recent stock report for LGA and Site level results
                    "balance": "{:,}".format(int(row['rutf_bal'])) if row['rutf_bal'] == row['rutf_bal'] else "No Data"
                })


        elif data_type == "site":
            # result = rate_by_week(result, df_filtered, 'siteid')
            kind = "siteid"
            number_of_inactive_sites, number_of_active_sites, adm_by_week, dead_rate_by_week, defu_rate_by_week,\
            dmed_rate_by_week, tout_rate_by_week, program_report_rate, stock_report_rate,\
            stock_by_week, two_weeks_margin = rate_by_week(df_filtered, df_stock_filtered, df_warehouse_filtered, kind, num)

            level = Site.objects.get(siteid=num)
            title = "%s,  %s-LGA %s " % (level.sitename,
                                         level.lga_num.lga.title(),
                                         level.state_num.state)
        else:
            raise Exception("We have encountered a datatype that we don't know how to handle: %s" % data_type)

    categories = []

    selected_year = year


    if current_year == selected_year:
        for week_iterator in range(1, current_week + 1):
            categories.append(iso_to_gregorian(current_year, week_iterator))
    elif current_year > selected_year:      # Previous years
        for week_iterator in range(1, weeks_for_year(selected_year) + 1):
            categories.append(iso_to_gregorian(selected_year, week_iterator))

    # Code below zips together data with correct week number so that missing data is presented correctly in highcharts
    def fill_empty_entries(to_fill):
        filled_list = []
        to_fill = dict(zip([iso_to_gregorian(selected_year, x) for x in to_fill.index.levels[1]], to_fill))
        for category in categories:
            if category in to_fill and not np.isnan(to_fill[category]):
                filled_list.append(to_fill[category])
            else:
                filled_list.append(None)

        return filled_list

    adm_by_week = fill_empty_entries(adm_by_week)
    stock_by_week = fill_empty_entries(stock_by_week) if len(stock_by_week) else []

    # here two_weeks_margin is a dictionary where the keys are timestamp like in the categories list
    two_weeks_margin = [two_weeks_margin.get(x) if x == x else None for x in categories]

    dead_rate_by_week = fill_empty_entries(dead_rate_by_week)
    defu_rate_by_week = fill_empty_entries(defu_rate_by_week)
    dmed_rate_by_week = fill_empty_entries(dmed_rate_by_week)
    tout_rate_by_week = fill_empty_entries(tout_rate_by_week)


    # return HttpResponse(json.dumps(result)
    return {
        "categories": categories,
        "adm_by_week": adm_by_week,
        "management_level": site_level,
        "dead_rate_by_week": dead_rate_by_week,
        "defu_rate_by_week": defu_rate_by_week,
        "dmed_rate_by_week": dmed_rate_by_week,
        "tout_rate_by_week": tout_rate_by_week,
        "number_of_inactive_sites": number_of_inactive_sites,
        "number_of_active_sites": number_of_active_sites,
        "stock_by_week": map(lambda x: float("%2.1f" % x) if x is not None else x, stock_by_week),
        "two_weeks_margin": two_weeks_margin,
        "program_report_rate": "%2.1f" % program_report_rate,
        "stock_report_rate": "%2.1f" % stock_report_rate,
        "recent_stock_report": recent_stock_report,
        "title": title,
        "date": date.today().strftime("%d-%m-%Y"),
    }


# kind = the level -  national, state, LGA or site
# num is the state_num, lga_num or siteid
# preferable to be explict than implicit, for example:
# present results on state level with state_num of 2
# present results on lga level with lga_num of 202
# present results on site level with siteid of 202110001

# The rate_by_week function is used by program and stock reporting
def rate_by_week(df_filtered, df_stock_filtered, df_warehouse_filtered, kind=None, num=None):
    # this is national level, no query
    if kind is None:
        df_queried = df_filtered
        df_stock_queried = df_stock_filtered

    else:
        # take only the rows where the kind (level) is identified by the site id
        df_queried = df_filtered.query('%s==%s' % (kind, num))
        df_stock_queried = df_stock_filtered.query('%s==%s' % (kind, num))

    df_queried['year_weeknum'] = zip(df_queried['year'].map(int), df_queried['weeknum'].map(int))
    df_queried['iso_year_weeknum'] = df_queried['year_weeknum'].map(lambda x: Week(x[0], x[1]))

    df_stock_queried['year_weeknum'] = zip(df_stock_queried['year'].map(int), df_stock_queried['weeknum'].map(int))
    df_stock_queried['iso_year_weeknum'] = df_stock_queried['year_weeknum'].map(lambda x: Week(x[0], x[1]))

    year, week, _ = date.today().isocalendar()
    current_week = Week(year, week)
    
    # Calculate since_x_weeks
    # Can we use same variable for both program and stock reports ?  if we work with incomplete data, use fillna ?
    df_queried['since_x_weeks'] = df_queried['iso_year_weeknum'].map(lambda x: current_week - x)
    df_stock_queried['since_x_weeks'] = df_stock_queried['iso_year_weeknum'].map(lambda x: current_week - x)

    # percentage of complete reporting
    program_report_rate = df_queried.query('since_x_weeks>0')\
                            .query('since_x_weeks<=8')\
                            .groupby(['siteid', 'type'])['weeknum']\
                            .count().map(lambda x: (x / 8.) * 100)\
                            .mean()

    stock_report_rate = df_stock_queried.query('since_x_weeks>0')\
                                        .query('since_x_weeks<=8')\
                                        .groupby(['siteid', 'type'])['weeknum']\
                                        .count()\
                                        .map(lambda x: (x / 8.) * 100)\
                                        .mean()

    # Set report_rates to zero if equal NaN
    program_report_rate = 0 if np.isnan(program_report_rate) else program_report_rate
    stock_report_rate = 0 if np.isnan(stock_report_rate) else stock_report_rate


    #FIXME add stock reports to algorithm to determine active sites.
    # Last_seen should go in the site database - then query site database if last_seen < 8 weeks = Active
    # State and LGA are always considered active, should always receive reports, but are not reported as active or inactive
    active_sites = df_queried.query('since_x_weeks<=8')\
                             .query('siteid>101110001')\
                             .groupby(['siteid', 'type'])\
                             ['siteid'].unique()\
                             .to_frame()\
                             .drop('siteid', axis=1)\
                             .reset_index()

    all_sites = df_queried.query('siteid>101110001')\
                          .groupby(['siteid', 'type'])\
                          ['siteid'].unique()\
                          .to_frame()\
                          .drop('siteid', axis=1)\
                          .reset_index()

    if len(active_sites) > 0:
        number_of_inactive_sites = len(set(zip(all_sites['siteid'],\
                                               all_sites['type'])) - set(zip(active_sites['siteid'],\
                                               active_sites['type'])))
        number_of_active_sites = len(active_sites)
    else:
        number_of_inactive_sites = None
        number_of_active_sites = None

    # Admissions and stock balance by week
    adm_by_week = df_queried['amar'].groupby([df_queried['year'], df_queried['weeknum']]).sum()

    if kind in ("lga_num", "state_num", None):
        if kind is not None:
            site_df = df_stock_queried.query('siteid > 199990999').query("%s==%s" % (kind, num))
            df_warehouse_queried = df_warehouse_filtered.query("siteid==%s" % num)
            stock_by_week = df_warehouse_queried['rutf_bal'].groupby([df_warehouse_queried['year'],\
                                                                      df_warehouse_queried['weeknum']])\
                                                                      .sum()
        else:
            site_df = df_stock_queried
            df_warehouse_queried = df_warehouse_filtered
            stock_by_week = []

        two_weeks_margin = {}

        max_since_x_weeks = site_df['since_x_weeks'].max()

        for i in sorted(site_df['since_x_weeks'].unique()):
            if i > max_since_x_weeks:
                break

            isoweek = site_df.query('since_x_weeks >= %s & since_x_weeks < (%s + 8)' % (i, i)).groupby('siteid')['iso_year_weeknum'].max().max()
            rutf_out = site_df.query('since_x_weeks >= %s & since_x_weeks < (%s + 8)' % (i, i)).groupby('siteid')['rutf_out'].median().sum()

            isoweek = iso_to_gregorian(isoweek.year, isoweek.week)

            if isoweek not in two_weeks_margin:
                two_weeks_margin[isoweek] = rutf_out if rutf_out == rutf_out else 0
            else:
                two_weeks_margin[isoweek] = two_weeks_margin[isoweek] + (rutf_out if rutf_out == rutf_out else 0)


    else:  # site level
        stock_by_week = df_stock_queried['rutf_bal'].groupby([df_stock_queried['year'], df_stock_queried['weeknum']]).sum()

        # Median RUTF use over past 8 weeks by week
        max_since_x_weeks = df_stock_queried['since_x_weeks'].max()

        # calculate the 2 weeks margin using a moving window
        two_weeks_margin = {}

        for i in sorted(df_stock_queried['since_x_weeks'].unique()):
            # only valid if year == 2016
            if i > max_since_x_weeks:
                break

            # FIXME
            # 8 week window is cut into less than 8 weeks when the dataframe is filtered by year
            # producing medians based on 7,6,5,4,3,2,1 weeks - Can see effect of median distorted by extreme values
            # run the two weeks margin calculation on the entire clean dataframe and store result in tuple?
            # run the two weeks margin calculation on the entire clean dataframe before running year filter?

            iso_year_weeknum = df_stock_queried.query('since_x_weeks >= %s & since_x_weeks < (%s + 8)' % (i, i))['iso_year_weeknum'].max()
            margin = df_stock_queried.query('since_x_weeks >= %s & since_x_weeks < (%s + 8)' % (i, i))['rutf_out'].median()
            two_weeks_margin[iso_to_gregorian(iso_year_weeknum.year, iso_year_weeknum.week)] = margin if margin == margin else None


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

    #FIXME change report_rate to program_rate_rate
    return number_of_inactive_sites, number_of_active_sites, adm_by_week, dead_rate_by_week, defu_rate_by_week,\
           dmed_rate_by_week, tout_rate_by_week, program_report_rate, stock_report_rate, stock_by_week, two_weeks_margin


# Query database and create data for admissions graph
def adm(request):
    current_year, current_week, _ = date.today().isocalendar()

    selected_year = int(request.GET.get("year", current_year))

    if "site_filter" not in request.GET or request.GET['site_filter'] in ("", "null"):
        data_type, num = "National", None
    else:
        data_type, num = request.GET['site_filter'].split('-', 1)

    # Filter by Site Type (all, outpatients OTP, inpatients IPF or SC)
    if "site_type" not in request.GET or request.GET['site_type'] == "All" or request.GET['site_type'] not in ("OTP", "SC"):
        site_type = "All"
    elif request.GET['site_type'] == "OTP":
        site_type = "OTP"
    elif request.GET['site_type'] == "SC":
        site_type = "SC"
    else:
        raise Exception("This site_type value is not permitted: %s" % request.GET['site_type'])

    data = json_for_charts(year=selected_year, site_level=data_type, siteid=num, site_type=site_type)

    # return HttpResponse(json.dumps(result)
    return HttpResponse(json.dumps(data))




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