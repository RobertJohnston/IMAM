from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import numpy as np
import pandas_highcharts.core
from sqlalchemy import create_engine

# Read data into dataframe

# This is the problem that crashes project.

engine = create_engine('postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
df = pd.read_sql_query("select * from program;", con=engine)

# fake data in data frame to use
# df = pd.DataFrame({'amar': np.random.randn(5)*100})


def index(request):

    # adm_by_week = df['amar'].groupby(df['weeknum']).mean()
    adm_by_week = df
    chart = pandas_highcharts.core.serialize(adm_by_week, render_to='my-chart',output_type='json')
    # module object has no attribute serialize unless you specify pandas except with pandas_highcharts.core

    return render(request, 'home/index.html')

# USING HTML.to_html

#def index(request):
#    return render_to_response('home/index.html', {'html.table': html_table}, RequestContext(request))

# create table to show in HTML
#crosstab = pd.crosstab(df['post'],df['type'],margins=True)
#html_table = crosstab.to_html(index=False)


