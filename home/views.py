from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import numpy as np
import pandas_highcharts.core
from sqlalchemy import create_engine





def index(request):

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

    adm_by_week = df_filtered['amar'].groupby(df_filtered['weeknum']).sum()

    chart = pandas_highcharts.core.serialize(adm_by_week.to_frame(), render_to='my-chart',output_type='json')
    # module object has no attribute serialize unless you specify pandas except with pandas_highcharts.core

    return render(request, 'home/index.html', {
        "chart": chart,
    })

# USING HTML.to_html

#def index(request):
#    return render_to_response('home/index.html', {'html.table': html_table}, RequestContext(request))

# create table to show in HTML
#crosstab = pd.crosstab(df['post'],df['type'],margins=True)
#html_table = crosstab.to_html(index=False)


