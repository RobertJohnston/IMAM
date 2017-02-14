from django.conf.urls import url

from . import views

app_name = 'map'
urlpatterns = [
    # url(r'^$', views.index, name='index' ),
    url(r'^$', views.map, name='map'),
    url(r'^map/', views.map, name='map'),
]


# app_name = 'polls'
# urlpatterns = [
#     # ex: /polls/
#     url(r'^$', views.IndexView.as_view(), name='index'),