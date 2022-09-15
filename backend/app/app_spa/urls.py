from django.urls import path, re_path, include
from app_spa import views

app_name = 'app_spa'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]