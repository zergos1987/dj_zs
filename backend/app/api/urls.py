from django.conf.urls import include, url
from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]