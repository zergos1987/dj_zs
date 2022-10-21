from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.contrib import messages
from app_accounts.models import ConnectionRequestsUrlsAndPermissions
from django.db.models import Q

def request_validate_url_access(self, request):
    request_url = request.path[1:]

    if len(request_url) == 0:
        request_url = '/'
    else:
        if request_url[-1] != '/':
            request_url += '/'

    if "admin/" not in request_url and not request.user.is_superuser:
        has_access = False
        text = "403 Forbidden"

        url_filter = (Q(url=request_url) &
                      Q(url_include_nested_urls=False))
        obj_url_permission = ConnectionRequestsUrlsAndPermissions.objects.filter(url_filter).first()

        if not obj_url_permission:
            request_url_parts = request_url.split('/')
            request_url_parts = list(filter(("").__ne__, request_url_parts))
            if len(request_url_parts) > 1:
                tmp_list = []
                j = 0
                for idx, i in enumerate(request_url_parts):
                    if j == 0:
                        v = request_url_parts[idx-j]
                        tmp_list.append(v+"/")
                    else:
                        v = request_url_parts[idx-j]
                        for f in range((idx+1)-j, idx+1):
                            v += "/" + request_url_parts[f]
                        tmp_list.append(v+"/")
                    j += 1
                request_url_parts = tmp_list
                request_url_parts_filter = "Q(" + ' | '.join([f"Q(url=request_url_parts[{i}])" for i in range(0, len(request_url_parts))]) + ")"
                url_filter = (eval(request_url_parts_filter) &
                              Q(url_include_nested_urls=True))
            else:
                url_filter = (Q(url=request_url) &
                              Q(url_include_nested_urls=True))

            obj_url_permission = ConnectionRequestsUrlsAndPermissions.objects.filter(url_filter).first()

        if obj_url_permission:
            url_has_access_anonymous = obj_url_permission.users_include_anonymous
            url_has_access_users = list(obj_url_permission.access_via_users.values_list('id', flat=True))
            url_has_access_roles = list(obj_url_permission.access_via_roles.values_list('name', flat=True))

            if request.user.is_anonymous:
                if url_has_access_anonymous:
                    has_access = True
            elif hasattr(request.user, 'id'):
                # No access restrictions by Users or Roles
                if len(url_has_access_users) == 0 and len(url_has_access_roles) == 0:
                    has_access = True
                # Users + Roles
                elif len(url_has_access_users) > 0 and len(url_has_access_roles) > 0:
                    if request.user.id in url_has_access_users:
                        if len(url_has_access_roles) > 0:
                            user_roles = list(request.user.groups.values_list('name', flat=True))
                            if len(user_roles) > 0:
                                for i in user_roles:
                                    if i in url_has_access_roles:
                                        has_access = True
                                        break
                        else:
                            has_access = True
                # Only Roles
                elif len(url_has_access_roles) > 0:
                    user_roles = list(request.user.groups.values_list('name', flat=True))
                    if len(user_roles) > 0:
                        for i in user_roles:
                            if i in url_has_access_roles:
                                has_access = True
                                break
                # Only Users
                else:
                    if len(url_has_access_users) > 0:
                        if request.user.id in url_has_access_users:
                            has_access = True

            # print(request.user.is_anonymous, url_has_access_anonymous)
            # print(url_has_access_users)
            # print(url_has_access_roles)
            # print(user_roles)

        if not has_access:
            user_id = "0"
            if hasattr(request.user, 'id'):
                if not request.user.is_anonymous:
                    user_id = str(request.user.id)
            claim_id = f"0-{user_id}"
            message_text = f'<div style="font-size: 0.3em; font-weight: 600">[ Claim id: {claim_id} ]</div><div style="padding-top: 5px; text-decoration: overline;">$$$message_text$$$</div>'
            message_template = f'<div style="display: flex; flex-direction: column;font-size: 2.2em; padding: 5% 0% 0% 7%;">$$$message_text$$$</div>'
            message_template = message_template.replace("$$$message_text$$$",
                                                        message_text.replace("$$$message_text$$$", text))
            response = HttpResponse(message_template)
            response.status_code = 403
            return response
