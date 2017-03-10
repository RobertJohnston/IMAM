import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import time
import numpy as np

from sqlalchemy import create_engine
from management.commands.load_data import assign_state_lga_num

from models import First_admin, Second_admin, Site

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
    for i in ('weeknum', 'state_num', 'lga_num', 'siteid', 'amar', 'dcur', 'dead', 'defu', 'dmed', 'tout'):
        df_filtered = df_filtered.query('%s==%s' % (i, i)).query('%s>=0' % i)
        # line below deletes entire row where a NaN is found
        # THIS IS ERROR IN DATA CLEANING - should leave in NaN
        # This does not remove all NaN

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

    # For all exit rate calculations see Final Report Consensus Meeting on M&E IMAM December 2010

    #####
    # Exit rates at national level are not correct
    # other exit rates at lower level are not correct as denominator is only at national level.
    #####

    # Total Discharges from program
    df_filtered['total_discharges'] = df_filtered.dcur + df_filtered.dead + df_filtered.defu + df_filtered.dmed

    # Total Exits from implementation site - Cout (Mike Golden term) includes the internal transfers - tout
    df_filtered['cout'] = df_filtered.total_discharges + df_filtered.tout

    # DCUR
    # df_filtered['dcur_rate'] = df_filtered.dcur / df_filtered.total_discharges
    # # DEAD
    # df_filtered['dead_rate'] = df_filtered.dead / df_filtered.total_discharges
    # # DEFU
    # df_filtered['defu_rate'] = df_filtered.defu / df_filtered.total_discharges
    # # DMED
    # df_filtered['dmed_rate'] = df_filtered.dmed / df_filtered.total_discharges
    # # TOUT
    # df_filtered['tout_rate'] = df_filtered.tout / df_filtered.cout

    # default or national level
    if "site_filter" not in request.GET or request.GET['site_filter'] == "":
        adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()

        # This method is almost correct - should be sum of deaths by week over total discharges by week *100
        dead_rate_by_week = df_filtered['dead'].groupby(df_filtered['weeknum']).sum() / df_filtered['total_discharges'].groupby(df_filtered['weeknum']).sum() *100
        defu_rate_by_week = df_filtered['defu'].groupby(df_filtered['weeknum']).sum() / df_filtered['total_discharges'].groupby(df_filtered['weeknum']).sum() *100
        dmed_rate_by_week = df_filtered['dmed'].groupby(df_filtered['weeknum']).sum() / df_filtered['total_discharges'].groupby(df_filtered['weeknum']).sum() *100
        tout_rate_by_week = df_filtered['tout'].groupby(df_filtered['weeknum']).sum() / df_filtered['cout'].groupby(df_filtered['weeknum']).sum() *100

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
            adm_by_week = df_filtered.query('state_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
            # in line below, django expects only one = to get value.
            first_admin = First_admin.objects.get(state_num=num)

            filter_discharge = df_filtered.query('state_num==%s' % num)['total_discharges'].groupby(df_filtered['weeknum']).sum()
            filter_cout = df_filtered.query('state_num==%s' % num)['cout'].groupby(df_filtered['weeknum']).sum()

            dead_rate_by_week = df_filtered.query('state_num==%s' % num)['dead'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            defu_rate_by_week = df_filtered.query('state_num==%s' % num)['defu'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            dmed_rate_by_week = df_filtered.query('state_num==%s' % num)['dmed'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            tout_rate_by_week = df_filtered.query('state_num==%s' % num)['tout'].groupby(df_filtered['weeknum']).sum() / filter_cout *100

            title = "%s %s" % (first_admin.state, data_type.capitalize())

        elif data_type == "lga":
            adm_by_week = df_filtered.query('lga_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
            second_admin = Second_admin.objects.get(lga_num=num)

            filter_discharge = df_filtered.query('lga_num==%s' % num)['total_discharges'].groupby(df_filtered['weeknum']).sum()
            filter_cout = df_filtered.query('lga_num==%s' % num)['cout'].groupby(df_filtered['weeknum']).sum()

            dead_rate_by_week = df_filtered.query('lga_num==%s' % num)['dead'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            defu_rate_by_week = df_filtered.query('lga_num==%s' % num)['defu'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            dmed_rate_by_week = df_filtered.query('lga_num==%s' % num)['dmed'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            tout_rate_by_week = df_filtered.query('lga_num==%s' % num)['tout'].groupby(df_filtered['weeknum']).sum() / filter_cout *100

            title = "%s-LGA %s" % (second_admin.lga.title(),
                                   second_admin.state_num.state.title())

        elif data_type == "site":
            adm_by_week = df_filtered.query('siteid==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
            site_level = Site.objects.get(siteid=num)

            filter_discharge = df_filtered.query('siteid==%s' % num)['total_discharges'].groupby(df_filtered['weeknum']).sum()
            filter_cout = df_filtered.query('siteid==%s' % num)['cout'].groupby(df_filtered['weeknum']).sum()

            dead_rate_by_week = df_filtered.query('siteid==%s' % num)['dead'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            defu_rate_by_week = df_filtered.query('siteid==%s' % num)['defu'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            dmed_rate_by_week = df_filtered.query('siteid==%s' % num)['dmed'].groupby(df_filtered['weeknum']).sum() / filter_discharge *100
            tout_rate_by_week = df_filtered.query('siteid==%s' % num)['tout'].groupby(df_filtered['weeknum']).sum() / filter_cout *100

            title = "%s,  %s-LGA %s " % (site_level.sitename.title(),
                                        site_level.lga_num.lga.title(),
                                        site_level.state_num.state.title())

        else:
            raise Exception("We have encountered a datatype that we don't know how to handle: %s" % data_type)

    adm_by_week = list(zip(adm_by_week.index, adm_by_week.values.tolist()))

    dead_rate_by_week = list(zip(dead_rate_by_week.index, dead_rate_by_week.values.tolist()))
    defu_rate_by_week = list(zip(defu_rate_by_week.index, defu_rate_by_week.values.tolist()))
    dmed_rate_by_week = list(zip(dmed_rate_by_week.index, dmed_rate_by_week.values.tolist()))
    tout_rate_by_week = list(zip(tout_rate_by_week.index, tout_rate_by_week.values.tolist()))


    return HttpResponse(json.dumps({
        "adm_by_week": adm_by_week,
        "dead_rate_by_week": dead_rate_by_week,
        "defu_rate_by_week": defu_rate_by_week,
        "dmed_rate_by_week": dmed_rate_by_week,
        "tout_rate_by_week": tout_rate_by_week,
        "title": title,
        # "date": date,
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





