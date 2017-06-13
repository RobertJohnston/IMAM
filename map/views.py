import json
from datetime import datetime

from isoweek import Week

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from home.models import Site

import time

# Create your views here.
def map(request):

    adm_dict = {'date': time.strftime("%d/%m/%y")}

    return render(request, 'map/map.html', context=adm_dict )
    #return render(request, 'map.html', {'content': ['Insert Map here']})
    # after the template dir add the map dir to correctly identify the path


def sites_gps_data(request):
    today_year, today_week, _ = datetime.now().isocalendar()

    def isoweek_diff(latest_program_last_seen):
        year, week, _ = latest_program_last_seen.isocalendar()
        return Week(today_year, today_week) - Week(year, week)

    sites_latest_program_date = {x.siteid: isoweek_diff(x.latest_program_last_seen) for x in Site.objects.raw("""
    select
        site.siteid,
        site.sitename,
        max(program.last_seen) as latest_program_last_seen
    from
        site,
        program
    where
        site.siteid = program.siteid
        and x_long is not NULL
        and y_lat is not NULL
    group by
        site.siteid;""")}

    with connection.cursor() as cursor:
        cursor.execute("""
        select
            siteid
        from
            site
        where
            site.siteid in (select distinct siteid from registration)
        """)
        sites_has_program = {x[0] for x in cursor.fetchall()}

    data = [
    {
        "sitename": x.sitename,
        "x_long": x.x_long,
        "y_lat": x.y_lat,
        "otp": x.otp,
        "sc": x.sc,
        "active": sites_latest_program_date.get(x.siteid, 999) <= 8
    } for x in Site.objects.filter(x_long__isnull=False, y_lat__isnull=False) if x.siteid in sites_has_program]

    return HttpResponse(json.dumps(data, indent=4))