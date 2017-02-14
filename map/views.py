from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def map(request):
    return render(request, 'map.html', )
    #return render(request, 'map.html', {'content': ['Insert Map here']})


# def contact(request):
#     return render(request, 'personal/basic.html', {'content':[' If you would like to contact me, please email me at slogojojo@gojira,np']})
