from django.shortcuts import render
from django.http import HttpResponse

import time

# Create your views here.
def map(request):

    adm_dict = {'date': time.strftime("%d/%m/%y")}

    return render(request, 'map/map.html', context=adm_dict )
    #return render(request, 'map.html', {'content': ['Insert Map here']})
    # after the template dir add the map dir to correctly identify the path


