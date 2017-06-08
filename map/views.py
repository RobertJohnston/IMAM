import json

from django.shortcuts import render
from django.http import HttpResponse

from home.models import Site

import time

# Create your views here.
def map(request):

    adm_dict = {'date': time.strftime("%d/%m/%y")}

    return render(request, 'map/map.html', context=adm_dict )
    #return render(request, 'map.html', {'content': ['Insert Map here']})
    # after the template dir add the map dir to correctly identify the path


def sites_gps_data(request):
    data = [{"sitename": x.sitename, "x_long": x.x_long, "y_lat": x.y_lat}
        for x in Site.objects.filter(x_long__isnull=False, y_lat__isnull=False)]
    return HttpResponse(json.dumps(data, indent=4))