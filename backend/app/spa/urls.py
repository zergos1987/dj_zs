from django.conf.urls import include, url
from django.urls import path
from spa import views

app_name = 'spa'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]