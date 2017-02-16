from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def map(request):

    adm_dict = {'garbage': "Pass the vulnuisbak, ASB"}

    return render(request, 'map/map.html', context=adm_dict )
    #return render(request, 'map.html', {'content': ['Insert Map here']})


