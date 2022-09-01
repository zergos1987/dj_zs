from django.urls import path, re_path, include
from spa import views

app_name = 'spa'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]