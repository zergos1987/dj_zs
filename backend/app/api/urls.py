from django.urls import path, re_path, include
from api import views

app_name = 'api'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]