from django.conf.urls import url

from . import views

app_name = 'map'
urlpatterns = [
    # url(r'^$', views.index, name='index' ),
    url(r'^$', views.map, name='map'),
    url(r'^sites.json', views.sites_gps_data, name='sites_gps_data'),
]


# app_name = 'polls'
# urlpatterns = [
#     # ex: /polls/
#     url(r'^$', views.IndexView.as_view(), name='index'),