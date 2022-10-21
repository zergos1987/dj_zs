from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from app_spa.models import pages_and_urls
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.cache import never_cache
from csp.decorators import csp_exempt


# Create your views here.



# def index(request, *args, **kwargs):
#     if not app_settings.objects.first():
#         record = app_settings.objects.create()
#         record.save()
#
#     if request.user.is_authenticated:
#         user_settings = app_settings.objects.filter(user=request.user).first()
#         if not user_settings:
#             record = app_settings.objects.create()
#             record.user = request.user
#             record.save()
#             user_settings = record
#     else:
#         user_settings = app_settings.objects.filter(user__isnull=True).first()
#
#     context = {
#         'app_settings': user_settings.json_data,
#     }
#     template = 'spa/index.html'
#
#     return render(request, template, context)
#
#
# def get_app_json_variable(name, user_id):
#     return 1
#
#
# def update_app_json_variable(name, user_id, init_variable, current_variable):
#     return 1
def get_ulr_level_datatypes(list_data):
    for idx, i in enumerate(list_data):
        try:
            int(i)
            list_data[idx] = "int"
        except ValueError:
            list_data[idx] = "str"
    return list_data


# @csp_exempt
@never_cache
def index(request,
          lvl_1=None, lvl_2=None, lvl_3=None, lvl_4=None, lvl_5=None,
          lvl_6=None, lvl_7=None, lvl_8=None, lvl_9=None, lvl_10=None,
          lvl_11=None, lvl_12=None, lvl_13=None, lvl_14=None, lvl_15=None,
          lvl_16=None, lvl_17=None, lvl_18=None, lvl_19=None, lvl_20=None,
          *args, **kwargs):
    is_process_data_request = (
            request.META.get('HTTP_X_REQUESTED_WITH', False) == 'XMLHttpRequest' and request.method == 'POST'
    )

    # App call init data request
    if not is_process_data_request:
        template = 'spa/index.html'
        return render(request, template)

    # App send process data request
    client_url_request = request.path
    client_url_request_levels = list(filter(None, client_url_request.split('/')))
    client_url_request_level_types = get_ulr_level_datatypes(client_url_request_levels.copy())
    print(client_url_request)
    print(client_url_request_levels)
    print(client_url_request_level_types)
    print(request.user.is_authenticated)
    # get init server_data for request session
    if request.user.is_authenticated:
        #server_data = user_pages_and_urls.objects.filter(user=request.user, url=client_url_request).first()
        server_data = {}
    else:
        server_data = pages_and_urls.objects.filter(url=client_url_request).first()

    # hide important key names for client side use
    if server_data:
        server_data["crb"] = server_data.pop("client_request_block")
        server_data["crd"] = server_data.pop("client_request_debounce")
        server_data["crp"] = server_data.pop("client_redirect_page")

    # return Server error page if cannot get server_data
    if not server_data:
        user_request = pages_and_urls.objects.filter(url="/server_error/").first()
        server_data = {}
        # server_data["crb"] = user_request.data_json["page"]["client_request_block"]
        # server_data["crd"] = user_request.data_json["page"]["client_request_debounce"]
        server_data["crp"] = '/' + request.resolver_match.app_name.replace('app_', '') + user_request.url
        print(server_data, 'FFFFFFFFF', request.resolver_match.app_name)
        # client_redirect_page = "/server_error/"
        # client_request_block = 1
        # client_request_debounce = 3000
        # server_data["crb"] = client_request_block
        # server_data["crd"] = client_request_debounce
        # server_data["crp"] = client_redirect_page


    return JsonResponse(server_data)
