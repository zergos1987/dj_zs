from app_accounts.models import ConnectionRequests, ConnectionRequests_BanUsers
from django.db.models import Q
from django.db.models.functions import Length
from django.contrib.gis.geoip2 import GeoIP2
from django_user_agents.utils import get_user_agent
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import datetime
from django.utils import timezone
import hashlib
from django.http import HttpResponse


def generate_id_for_list_of_columns(columns, size=5):
    unique_id = ""
    for s in columns:
        if s is None: s = '-'
        if type(s).__name__ == 'bool': s = str(s)
        if type(s).__name__ == 'int': s = str(s)
        unique_id += s
    unique_id = hashlib.sha1(str.encode(unique_id)).hexdigest()
    return unique_id


def request_get_connection_columns(request, exclude_columns_from_unique_id=[]):
    """
        user request id columns formatting and validating for creating unique id
    """
    columns = {}

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        request_ip = x_forwarded_for.split(',')[0]
    else:
        request_ip = request.META.get('REMOTE_ADDR')

    request_count = 1

    user_agent = get_user_agent(request)

    request_user_agent_browser_family = user_agent.browser.family
    request_user_agent_browser_version = user_agent.browser.version_string
    request_user_agent_device_family = user_agent.device.family
    request_user_agent_device_brand = user_agent.device.brand
    request_user_agent_device_model = user_agent.device.model
    request_user_agent_is_email_client = user_agent.is_email_client
    request_user_agent_is_mobile = user_agent.is_mobile
    request_user_agent_is_pc = user_agent.is_pc
    request_user_agent_is_tablet = user_agent.is_tablet
    request_user_agent_is_touch_capable = user_agent.is_touch_capable
    request_user_agent_os_family = user_agent.os.family
    request_user_agent_os_version_string = user_agent.os.version_string
    request_user_agent_device_type = "request_user_agent_device_type"
    if request_user_agent_is_email_client:
        request_user_agent_device_type = "Email"
    if request_user_agent_is_mobile:
        request_user_agent_device_type = "Mobile"
    if request_user_agent_is_pc:
        request_user_agent_device_type = "PC"
    if request_user_agent_is_tablet:
        request_user_agent_device_type = "TABLET"
    if request_user_agent_is_touch_capable:
        request_user_agent_device_type = "TOUCH_SCREEN"
    request_session_key = request.session.session_key
    request_content_type = request.content_type
    request_get_full_path = request.get_full_path()
    request_connection_is_secure = request.is_secure()
    request_method = request.method
    request_user_id = "request_user_id"
    if hasattr(request.user, 'id'):
        if not request.user.is_anonymous:
            request_user_id = request.user.id
    request_user_is_anonymous = request.user.is_anonymous
    request_user_is_authenticated = request.user.is_authenticated
    if hasattr(request.user, 'last_login'):
        if not request.user.is_anonymous:
            request_user_last_login = request.user.last_login
            request_user_last_login_year = request_user_last_login.year
            request_user_last_login_month = request_user_last_login.month
            request_user_last_login_day = request_user_last_login.day
            request_user_last_login_hour = request_user_last_login.hour
            request_user_last_login_minute = request_user_last_login.minute
    else:
        request_user_last_login = "request_user_last_login"
        request_user_last_login_year = "request_user_last_login_year"
        request_user_last_login_month = "request_user_last_login_month"
        request_user_last_login_day = "request_user_last_login_day"
        request_user_last_login_hour = "request_user_last_login_hour"
        request_user_last_login_minute = "request_user_last_login_minute"

    # g = GeoIP2()
    # location = g.city(ip)
    # request_location_city = location.get("city")
    # request_location_continent_code = location.get("continent-code")
    # request_location_continent_name = location.get("continent-name")
    # request_location_code = location.get("country_code")
    # request_location_name = location.get("country_name")
    # request_location_dma_code = location.get("dma_code")
    # request_location_postal_code = location.get("postal-code")
    # request_location_latitude = location.get("latitude")
    # request_location_longitude = location.get("longitude")
    # request_location_region = location.get("region")
    # request_time_zone = location.get("time-zone")

    columns["request_count"] = request_count
    columns["request_ip"] = request_ip
    columns["request_user_agent_browser_family"] = request_user_agent_browser_family
    columns["request_user_agent_browser_version"] = request_user_agent_browser_version
    columns["request_user_agent_device_family"] = request_user_agent_device_family
    columns["request_user_agent_device_brand"] = request_user_agent_device_brand
    columns["request_user_agent_device_model"] = request_user_agent_device_model
    columns["request_user_agent_device_type"] = request_user_agent_device_type
    columns["request_user_agent_os_family"] = request_user_agent_os_family
    columns["request_user_agent_os_version_string"] = request_user_agent_os_version_string
    columns["request_content_type"] = request_content_type
    columns["request_get_full_path"] = request_get_full_path
    columns["request_connection_is_secure"] = request_connection_is_secure
    columns["request_method"] = request_method
    columns["request_user_id"] = request_user_id
    columns["request_user_is_anonymous"] = request_user_is_anonymous
    columns["request_user_is_authenticated"] = request_user_is_authenticated
    columns["request_session_key"] = request_session_key
    columns["request_user_last_login_year"] = request_user_last_login_year
    columns["request_user_last_login_month"] = request_user_last_login_month
    columns["request_user_last_login_day"] = request_user_last_login_day
    columns["request_user_last_login_hour"] = request_user_last_login_hour
    columns["request_user_last_login_minute"] = request_user_last_login_minute
    # columns["request_location_city"] = request_location_city
    # columns["request_location_continent_code"] = request_location_continent_code
    # columns["request_location_continent_name"] = request_location_continent_name
    # columns["request_location_country_code"] = request_location_country_code
    # columns["request_location_dma_code"] = request_location_dma_code
    # columns["request_location_postal_code"] = request_location_postal_code
    # columns["request_location_latitude"] = request_location_latitude
    # columns["request_location_longitude"] = request_location_longitude
    # columns["request_location_region"] = request_location_region
    # columns["request_time_zone"] = request_time_zone

    exclude_columns = {}
    exclude_columns_from_unique_id += ["request_count"]
    if len(exclude_columns_from_unique_id) > 0:
        exclude_columns = {k: v for k, v in columns.items() if k not in exclude_columns_from_unique_id}
    columns = {**{k: None for k, v in columns.items() if k == v}, **{k: v for k, v in columns.items() if k != v}}
    request_unique_id = generate_id_for_list_of_columns(columns=[*exclude_columns.values()], size=10)

    columns["request_unique_id"] = request_unique_id

    # for key, value in columns.items():
    #     print("Column name:", key, " --- dataType:", type(value).__name__, " --- value:", value)

    return columns


def request_validate_connection(self, request):
    response = None

    def update_request_history(request):

        columns = request_get_connection_columns(request=request, exclude_columns_from_unique_id=[
            "request_session_key",
            "request_user_last_login_year",
            "request_user_last_login_month",
            "request_user_last_login_day",
            "request_user_last_login_hour",
            "request_user_last_login_minute",
        ])

        # save current request properties
        request_obj_is_created = False
        obj = ConnectionRequests.objects.filter(request_unique_id=columns.get('request_unique_id')).first()
        if obj:
            # do nothing for now /  update request instance counters and others - below
            pass
        else:
            # create new request instance in db
            obj = ConnectionRequests.objects.create(**columns)
            request_obj_is_created = True

            # update previews request properties with current request properties
            if request.session.get("request_unique_id_parent", "") != "":
                if request.session.get("request_unique_id_parent") != columns.get('request_unique_id'):
                    child_obj = ConnectionRequests.objects.filter(request_unique_id=request.session.get("request_unique_id_parent"))
                    child_obj.update(request_unique_id_parent=obj)

            request.session["request_unique_id_parent"] = columns.get('request_unique_id')
            request.session.save()


        # check if request in ban list and if - add him to ban list
        if not bool(obj.request_restrict_object):
            # get base ban obj for user/anonymous and url/all urls
            user_filter = Q(user__isnull=True)
            if obj.request_user_id:
                user_filter = Q(user__id=obj.request_user_id)

            ban_objs = ConnectionRequests_BanUsers.objects.filter(
                Q(is_actual=True) &
                user_filter & (
                    Q(('{}__contains'.format("template_bans__limit_contains_request_get_full_path"),
                       columns.get('request_get_full_path'))) |
                    Q(template_bans__limit_contains_request_get_full_path__isnull=True)
                )
            ).all()

            # get filtered ban obj
            for i in ban_objs:
                limit_columns_for_restriction = str(i.template_bans.ban_template_selected_columns)
                limit_columns_for_restriction = limit_columns_for_restriction.split(",")
                limit_columns_for_restriction = [j for j in limit_columns_for_restriction
                                                 if j != "limit_contains_request_get_full_path" and "_count" not in j]

                extra_where_clauses_count = len(limit_columns_for_restriction)
                extra_where_clauses_count_verified = 0
                for restrict_column in limit_columns_for_restriction:
                    restrict_column_value = eval(f"i.template_bans.{restrict_column}")
                    if "limit_contains_" in restrict_column and columns.get(
                            restrict_column.replace("limit_contains_", "")) in restrict_column_value:
                        extra_where_clauses_count_verified += 1

                    if "limit_boolean_" in restrict_column and restrict_column_value == columns.get(
                            restrict_column.replace("limit_boolean_", "")):
                        extra_where_clauses_count_verified += 1

                if extra_where_clauses_count == extra_where_clauses_count_verified:
                    request_restrict_object = {}
                    if i.template_bans.limit_contains_request_get_full_path:
                        request_restrict_object["limit_contains_request_get_full_path"] = columns.get(
                            'request_get_full_path')
                    else:
                        request_restrict_object["limit_contains_request_get_full_path"] = ""
                    request_restrict_object["ban_id"] = i.id
                    request_restrict_object["limit_max_request_count"] = i.template_bans.limit_max_request_count
                    request_restrict_object["limit_max_request_count_per_minute"] = i.template_bans.limit_max_request_count_per_minute
                    request_restrict_object["limit_max_request_count_per_hour"] = i.template_bans.limit_max_request_count_per_hour
                    request_restrict_object["limit_max_request_count_per_day"] = i.template_bans.limit_max_request_count_per_day
                    request_restrict_object["limit_max_request_count_per_week"] = i.template_bans.limit_max_request_count_per_week
                    request_restrict_object["ban_is_permanent"] = i.ban_is_permanent
                    request_restrict_object["ban_minutes"] = i.ban_minutes
                    request_restrict_object["ban_message"] = i.ban_message
                    request_restrict_object["ban_datetime"] = str(datetime.datetime.now())

                    obj.request_restrict_object = request_restrict_object
                    break

        # execute ban if exists for request
        if bool(obj.request_restrict_object):
            ban_expired_at = datetime.datetime.strptime(
                obj.request_restrict_object.get("ban_datetime"), "%Y-%m-%d %H:%M:%S.%f")
            ban_expired_at = ban_expired_at + datetime.timedelta(
                minutes=obj.request_restrict_object.get("ban_minutes") * obj.request_restrict_object_applied_count)

            ban_is_valid = False
            ban_is_actual = True
            ban_text = ""

            if ConnectionRequests_BanUsers.objects.filter(id=obj.request_restrict_object.get("ban_id")).first().is_actual:
                if obj.request_restrict_object.get("ban_is_permanent") or \
                        obj.request_restrict_object.get("limit_max_request_count") == 0:
                    ban_text = "Your are blocked permanently on this url."
                    ban_is_valid = True
                else:
                    if ban_expired_at > datetime.datetime.now():
                        ban_text = f'Your are blocked till {ban_expired_at.strftime("%Y-%m-%d %H:%M:%S")}'
                        if obj.request_count >= (obj.request_restrict_object.get("limit_max_request_count") *
                                                 obj.request_restrict_object_applied_count):
                            ban_is_valid = True
                        if (obj.request_restrict_object.get("limit_max_request_count_per_minute") > 0) and \
                                (obj.request_count_per_minute >= obj.request_restrict_object.get("limit_max_request_count_per_minute")):
                            ban_is_valid = True
                        if (obj.request_restrict_object.get("limit_max_request_count_per_hour") > 0) and \
                                (obj.request_count_per_hour >= obj.request_restrict_object.get("limit_max_request_count_per_hour")):
                            ban_is_valid = True
                        if (obj.request_restrict_object.get("limit_max_request_count_per_day") > 0) and \
                                (obj.request_count_per_day >= obj.request_restrict_object.get("limit_max_request_count_per_day")):
                            ban_is_valid = True
                        if (obj.request_restrict_object.get("limit_max_request_count_per_week") > 0) and \
                                (obj.request_count_per_week >= obj.request_restrict_object.get("limit_max_request_count_per_week")):
                            ban_is_valid = True
                    else:
                        ban_is_actual = False
            else:
                ban_is_actual = False

            if not ban_is_valid and ban_is_actual:
                obj.request_restrict_object["ban_datetime"] = str(datetime.datetime.now())

            if ban_is_valid:
                user_id = "0"
                if hasattr(request.user, 'id'):
                    if not request.user.is_anonymous:
                        user_id = str(request.user.id)
                claim_id = f"{obj.request_restrict_object.get('ban_id')}-{user_id}"

                # save ban instance object for request
                obj.request_restrict_object["claim_id"] = claim_id
                obj.save(save_counters=False)

                # return ban message / redirect to ban view
                message_text = f'<div style="font-size: 0.3em; font-weight: 600">[ Claim id: {claim_id} ]</div><div style="padding-top: 5px; text-decoration: overline;">$$$message_text$$$</div>'
                message_template = f'<div style="display: flex; flex-direction: column;font-size: 2.2em; padding: 5% 0% 0% 7%;">$$$message_text$$$</div>'
                message_template = message_template.replace("$$$message_text$$$", message_text.replace("$$$message_text$$$", ban_text))
                response = HttpResponse(message_template)
                response.status_code = 403
                return response
                #raise PermissionDenied()
            else:
                if not request_obj_is_created:
                    obj.save(save_counters=True)
                else:
                    obj.save(save_counters=False)

            if not ban_is_actual:
                # clear ban obj from saved request instance in db
                ConnectionRequests_BanUsers.objects.filter(
                    id=obj.request_restrict_object.get("ban_id")).update(is_actual=False)
                obj.request_restrict_object = {}
                obj.request_restrict_object_applied_count += 1
                # update ban obj for exists saved request instance in db
                obj.save(save_counters=False)

        else:
            # update increment count and other props for exists saved request instance in db
            if not request_obj_is_created:
                obj.save(save_counters=True)


    if not request.user.is_superuser:
        response = update_request_history(request=request)

    return response
