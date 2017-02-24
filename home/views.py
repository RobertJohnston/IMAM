import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
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

    # Convert to float
    df['amar'] = pd.to_numeric(df.amar, errors='coerce')
    df['weeknum'] = pd.to_numeric(df.weeknum, errors='coerce')
    df['state_num'] = pd.to_numeric(df.state_num, errors='coerce')
    df['lga_num'] = pd.to_numeric(df.lga_num, errors='coerce')
    df['siteid'] = pd.to_numeric(df.siteid, errors='coerce')

    # Clean out of range data
    df_filtered = df.query('weeknum==weeknum').query('0<weeknum<53')
    df_filtered = df_filtered.query('amar==amar').query('0<amar<99999')
    df_filtered = df_filtered.query('state_num==state_num').query('0<state_num<37')
    df_filtered = df_filtered.query('lga_num==lga_num').query('101<lga_num<3799')
    df_filtered = df_filtered.query('siteid==siteid').query('101110001<siteid<3999999999')

    # Set to int - so that decimal points are not presented
    df_filtered['weeknum'] = df_filtered.weeknum.astype('int')
    df_filtered['amar'] = df_filtered.amar.astype('int')
    df_filtered['state_num'] = df_filtered.state_num.astype('int')
    df_filtered['lga_num'] = df_filtered.lga_num.astype('int')
    df_filtered['siteid'] = df_filtered.siteid.astype('int')


    # default or national level
    if "site_filter" not in request.GET or request.GET['site_filter'] == "":
        adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()

        data = list(zip(adm_by_week.index, adm_by_week.values.tolist()))
        return HttpResponse(json.dumps({
            "adm_by_week": data,
            "title": "National Level",
        }))

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
        title = "%s %s" % (first_admin.state, data_type)

    elif data_type == "lga":
        adm_by_week = df_filtered.query('lga_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
        second_admin = Second_admin.objects.get(lga_num=num)
        title = "%s %s" % (second_admin.lga, data_type)

    elif data_type == "site":
        adm_by_week = df_filtered.query('siteid==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
        site_level = Site.objects.get(siteid=num)
        title = "%s %s" % (site_level.sitename, data_type)

    data = list(zip(adm_by_week.index, adm_by_week.values.tolist()))

    return HttpResponse(json.dumps({
        "adm_by_week": data,
        "title": title,
    }))


def index(request):
    state_list = First_admin.objects.all().order_by('state_num')

    lga_list = Second_admin.objects.all().order_by('lga_num')

    site_list = Site.objects.all().order_by('siteid')

    return render(request, 'home/index.html', {"state_list": state_list,
                                               "lga_list": lga_list,
                                               "site_list": site_list,
                                               })


# USING HTML.to_html

#def index(request):
#    return render_to_response('home/index.html', {'html.table': html_table}, RequestContext(request))

# create table to show in HTML
#crosstab = pd.crosstab(df['post'],df['type'],margins=True)
#html_table = crosstab.to_html(index=False)


