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

    # Assign state and LGA numbers to data frame
    df = assign_state_lga_num(df)

    # Convert from string to float
    df['amar'] = pd.to_numeric(df.amar, errors='coerce')
    df['weeknum'] = pd.to_numeric(df.weeknum, errors='coerce')
    df['state_num'] = pd.to_numeric(df.state_num, errors='coerce')
    df['lga_num'] = pd.to_numeric(df.lga_num, errors='coerce')
    df['siteid'] = pd.to_numeric(df.siteid, errors='coerce')

    # Clean out of range data
    # It is appropriate to delete the entire row of data if there is no ID or week number
    # line below deletes entire row where a NaN is found - see all queries
    df_filtered = df.query('weeknum==weeknum').query('0<weeknum<53')
    df_filtered = df_filtered.query('state_num==state_num').query('0<state_num<37')
    df_filtered = df_filtered.query('lga_num==lga_num').query('101<lga_num<3799')
    df_filtered = df_filtered.query('siteid==siteid').query('101110001<siteid<3999999999')

    # Set to int - so that decimal points are not presented
    df_filtered['weeknum'] = df_filtered.weeknum.astype('int')
    df_filtered['state_num'] = df_filtered.state_num.astype('int')
    df_filtered['lga_num'] = df_filtered.lga_num.astype('int')
    df_filtered['siteid'] = df_filtered.siteid.astype('int')

    # Data cleaning for admissions
    df_filtered = df_filtered.query('amar==amar').query('0<amar<99999')
    df_filtered['amar'] = df_filtered.amar.astype('int')

    # Data cleaning for exit rates
    for i in ('dcur', 'dead', 'defu', 'dmed', 'tout'):
        df_filtered[i] = pd.to_numeric(df_filtered[i], errors='coerce')
        # line below deletes entire row where a NaN is found
        # THIS IS ERROR IN DATA CLEANING - should leave in NaN
        # This does not remove all NaN
        df_filtered = df_filtered.query('%s==%s' % (i, i)).query('0<=%s' % i)
        df_filtered[i] = df_filtered[i].astype(int)


    # For all calculations see Final Report Consensus Meeting on M&E IMAM December 2010

    # Total Discharges from program
    df_filtered['total_discharges'] = df_filtered.dcur + df_filtered.dead + df_filtered.defu + df_filtered.dmed

    # Total Exits from implementation site - Cout (Mike Golden term) includes the internal transfers - tout
    df_filtered['cout'] = df_filtered.total_discharges + df_filtered.tout


    # DCUR
    df_filtered['dcur_rate'] = df_filtered.dcur / df_filtered.total_discharges
    # DEAD
    df_filtered['dead_rate'] = df_filtered.dead / df_filtered.total_discharges
    # DEFU
    df_filtered['defu_rate'] = df_filtered.defu / df_filtered.total_discharges
    # DMED
    df_filtered['dmed_rate'] = df_filtered.dmed / df_filtered.total_discharges
    # TOUT
    df_filtered['tout_rate'] = df_filtered.tout / df_filtered.cout

    # default or national level
    if "site_filter" not in request.GET or request.GET['site_filter'] == "":
        adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()
        adm_by_week = list(zip(adm_by_week.index, adm_by_week.values.tolist()))

        dead_rate_by_week = df_filtered['dead_rate'].groupby(df_filtered['weeknum']).sum()
        dead_rate_by_week = list(zip(dead_rate_by_week.index, dead_rate_by_week.values.tolist()))

        defu_rate_by_week = df_filtered['defu_rate'].groupby(df_filtered['weeknum']).sum()
        defu_rate_by_week = list(zip(defu_rate_by_week.index, defu_rate_by_week.values.tolist()))

        dmed_rate_by_week = df_filtered['dmed_rate'].groupby(df_filtered['weeknum']).sum()
        dmed_rate_by_week = list(zip(dmed_rate_by_week.index, dmed_rate_by_week.values.tolist()))

        tout_rate_by_week = df_filtered['tout_rate'].groupby(df_filtered['weeknum']).sum()
        tout_rate_by_week = list(zip(tout_rate_by_week.index, tout_rate_by_week.values.tolist()))

        title = "National Level"

    else:
        # request format is: state-23, lga-333, siteid 101110001
        # Last input on split - only allow one split on request.GET to ensure dangerous user input
        data_type, num = request.GET['site_filter'].split('-', 1)
        # add name to datatype here

        # Always sanitize input for security
        # ideally we should is a django form here
        assert num.isdigit()

        if data_type == "state":
            adm_by_week = df_filtered.query('state_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
            # in line below, django expects only one = to get value.
            first_admin = First_admin.objects.get(state_num=num)
            dead_rate_by_week = df_filtered.query('state_num==%s' % num)['dead_rate'].groupby(df_filtered['weeknum']).sum()
            defu_rate_by_week = df_filtered.query('state_num==%s' % num)['defu_rate'].groupby(df_filtered['weeknum']).sum()
            dmed_rate_by_week = df_filtered.query('state_num==%s' % num)['dmed_rate'].groupby(df_filtered['weeknum']).sum()
            tout_rate_by_week = df_filtered.query('state_num==%s' % num)['tout_rate'].groupby(df_filtered['weeknum']).sum()

            title = "%s %s" % (first_admin.state, data_type.capitalize())

        elif data_type == "lga":
            adm_by_week = df_filtered.query('lga_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
            second_admin = Second_admin.objects.get(lga_num=num)
            dead_rate_by_week = df_filtered.query('lga_num==%s' % num)['dead_rate'].groupby(df_filtered['weeknum']).sum()
            defu_rate_by_week = df_filtered.query('lga_num==%s' % num)['defu_rate'].groupby(df_filtered['weeknum']).sum()
            dmed_rate_by_week = df_filtered.query('lga_num==%s' % num)['dmed_rate'].groupby(df_filtered['weeknum']).sum()
            tout_rate_by_week = df_filtered.query('lga_num==%s' % num)['tout_rate'].groupby(df_filtered['weeknum']).sum()

            title = "%s-LGA - %s" % (second_admin.lga, second_admin.state_num.state)

        elif data_type == "site":
            adm_by_week = df_filtered.query('siteid==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
            site_level = Site.objects.get(siteid=num)
            dead_rate_by_week = df_filtered.query('siteid==%s' % num)['dead_rate'].groupby(df_filtered['weeknum']).sum()
            defu_rate_by_week = df_filtered.query('siteid==%s' % num)['defu_rate'].groupby(df_filtered['weeknum']).sum()
            dmed_rate_by_week = df_filtered.query('siteid==%s' % num)['dmed_rate'].groupby(df_filtered['weeknum']).sum()
            tout_rate_by_week = df_filtered.query('siteid==%s' % num)['tout_rate'].groupby(df_filtered['weeknum']).sum()

            title = "%s %s-LGA %s " % (site_level.sitename.capitalize(),
                                              site_level.lga_num.lga.capitalize(),
                                              site_level.state_num.state.capitalize())

        else:
            raise Exception("We have encountered a datatype that we don't know how to handle: %s" % data_type)

        adm_by_week = list(zip(adm_by_week.index, adm_by_week.values.tolist()))
        dead_rate_by_week = list(zip(dead_rate_by_week.index, dead_rate_by_week.values.tolist()))
        defu_rate_by_week = list(zip(defu_rate_by_week.index, defu_rate_by_week.values.tolist()))
        dmed_rate_by_week = list(zip(dmed_rate_by_week.index, dmed_rate_by_week.values.tolist()))
        tout_rate_by_week = list(zip(tout_rate_by_week.index, tout_rate_by_week.values.tolist()))
        date = {'date': time.strftime("%d/%m/%y")}

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





