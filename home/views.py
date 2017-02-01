from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
from sqlalchemy import create_engine

# Read data into dataframe
engine = create_engine('postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
df = pd.read_sql_query("select * from registration;", con=engine)

# create table to show in HTML
crosstab = pd.crosstab(df['post'],df['type'],margins=True)
html_table = crosstab.to_html(index=False)

#def index(request):
#    return render_to_response('home/index.html', {'html.table': html_table}, RequestContext(request))

# Create your views here.
def index(request):
     return render(request, 'home/index.html')

