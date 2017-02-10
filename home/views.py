from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import numpy as np
import pandas_highcharts.core
from sqlalchemy import create_engine
from management.commands.load_data import assign_state_lga_num

def adm(request):
    # Read data into dataframe - at each function call

    engine = create_engine(
        'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
    df = pd.read_sql_query("select * from program;", con=engine)

    # Convert to float
    df['amar'] = pd.to_numeric(df.amar, errors='coerce')
    df['weeknum'] = pd.to_numeric(df.weeknum, errors='coerce')

    df_filtered = df.query('weeknum==weeknum').query('0<weeknum<53')
    df_filtered['weeknum'] = df_filtered.weeknum.astype('int')

    df_filtered = df_filtered.query('amar==amar').query('0<amar<99999')
    df_filtered['amar'] = df_filtered.amar.astype('int')

    df_filtered = assign_state_lga_num(df_filtered)
    df_filtered['state_num'] = pd.to_numeric(df_filtered.state_num, errors='coerce')
    df_filtered = df_filtered.query('state_num==state_num').query('0<state_num<37')
    df_filtered['state_num'] = df_filtered.state_num.astype('int')


    if "state_number" in request.GET:
        # TODO filter user input
        state_number = request.GET["state_number"]
        adm_by_week = df_filtered.query('state_num==%s' % state_number)['amar'].groupby(df_filtered['weeknum']).sum()
    else:
        adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()

    chart = pandas_highcharts.core.serialize(adm_by_week.to_frame(), render_to='my-chart',output_type='json')
    # module object has no attribute serialize unless you specify pandas except with pandas_highcharts.core

    return HttpResponse(chart)


def index(request):
    return render(request, 'home/index.html')

# USING HTML.to_html

#def index(request):
#    return render_to_response('home/index.html', {'html.table': html_table}, RequestContext(request))

# create table to show in HTML
#crosstab = pd.crosstab(df['post'],df['type'],margins=True)
#html_table = crosstab.to_html(index=False)


