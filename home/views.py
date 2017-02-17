from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import numpy as np
import pandas_highcharts.core
from sqlalchemy import create_engine
from management.commands.load_data import assign_state_lga_num
from models import Siteid

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

    # Clean out of range data
    df_filtered = df.query('weeknum==weeknum').query('0<weeknum<53')
    df_filtered = df_filtered.query('amar==amar').query('0<amar<99999')
    df_filtered = df_filtered.query('state_num==state_num').query('0<state_num<37')
    df_filtered = df_filtered.query('lga_num==lga_num').query('101<lga_num<3799')

    # Set to int - so that decimal points are not presented
    df_filtered['weeknum'] = df_filtered.weeknum.astype('int')
    df_filtered['amar'] = df_filtered.amar.astype('int')
    df_filtered['state_num'] = df_filtered.state_num.astype('int')
    df_filtered['lga_num'] = df_filtered.lga_num.astype('int')

    # default or national level
    if "state_number" not in request.GET or request.GET['state_number'] == "":
        adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()
        chart = pandas_highcharts.core.serialize(adm_by_week.to_frame(), render_to='my-chart', output_type='json')
        return HttpResponse(chart)

    # request format is: state-23 or lga-333
    data_type, num = request.GET['state_number'].split('-', 1)

    # sanitize input for security
    # ideally we should is a django form here
    assert num.isdigit()

    if data_type == "state":
        adm_by_week = df_filtered.query('state_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()
    elif data_type == "lga":
        adm_by_week = df_filtered.query('lga_num==%s' % num)['amar'].groupby(df_filtered['weeknum']).sum()

    chart = pandas_highcharts.core.serialize(adm_by_week.to_frame(), render_to='my-chart',output_type='json')

    return HttpResponse(chart)


def index(request):
    state_list = sorted(Siteid.objects.all().values('state', 'state_num').distinct(), key=lambda x: int(x['state_num']))

    lga_list = sorted(Siteid.objects.all().values('lga', 'lga_num').distinct(), key=lambda x: int(x['lga_num']))

    return render(request, 'home/index.html', {"state_list": state_list, "lga_list": lga_list })

# def index(request):
#     select_list = sorted(Siteid.objects.all().values('lga', 'lga_num').distinct(), key=lambda x: int(x['lga_num']))
#     return render(request, 'home/index.html', {"select_list": select_list})

# USING HTML.to_html

#def index(request):
#    return render_to_response('home/index.html', {'html.table': html_table}, RequestContext(request))

# create table to show in HTML
#crosstab = pd.crosstab(df['post'],df['type'],margins=True)
#html_table = crosstab.to_html(index=False)


