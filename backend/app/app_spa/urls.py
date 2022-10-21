from django.urls import path, re_path, include
from app_spa import views



app_name = 'app_spa'



urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]

def get_url_lvl_string(max_lvls_index=1):
    """ returns ' (?P<lvl_1>\w+)/(?P<lvl_2>\w+)/.../ '
        string value
    """
    lvls = list(range(1, 21))[0:max_lvls_index]
    url_lvl_string = ''.join(["(?P<lvl_{lvl}>\w+)/".format(lvl=i) for i in lvls])
    return url_lvl_string

for i in range(1, 11):
    urlpatterns += [
        re_path(r'^{url_lvl_string}$'.format(url_lvl_string=get_url_lvl_string(i)), views.index, name='index'),
    ]
