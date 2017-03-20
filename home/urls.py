from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index' ),
    url(r'^adm/', views.adm, name='adm'),
    url(r'^search/', views.search, name='search'),
]