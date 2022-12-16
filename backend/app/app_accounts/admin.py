from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Permission
from .models import (
        SessionExtraData,
        User,
        UserProfile,
        UserProfileFiles,
        ConnectionRequests,
        ConnectionRequestsUrlsAndPermissions,
        ConnectionRequests_BanTemplates,
        ConnectionRequests_BanUsers,
	)
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
import os



# Register your models here.



class UserResource(resources.ModelResource):
    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'username', 'email', 'phone',)
        #exclude = ('',)

class UserModelAdmin(UserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "updated_at", "created_at",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone", "password1", "password2", "is_active",),
            },
        ),
    )
    list_display = ("id", "username", 'email', 'phone', "is_active",)
    list_filter = (
        "is_staff", "is_superuser", "is_active", "groups",
        ('date_joined', DateTimeRangeFilter),
    )
    search_fields = ("username", 'email', 'phone',)
    readonly_fields = ("last_login", "date_joined", "updated_at", "created_at",)
    ordering = ("date_joined",)
    list_per_page = 10
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def save_model(self, request, obj, form, change):
        super(UserModelAdmin, self).save_model(request, obj, form, change)

    def has_import_permission(self, request, obj=None):
        return True

    def has_export_permission(self, request, obj=None):
        return True

    resource_class = UserResource



def get_profile_avatar(obj):
    if obj.pk:
        return mark_safe(
            f"""<a href="{obj.profile_avatar.url}" target="_blank">
            <img src="{obj.profile_avatar.url}" alt="avatar" style="max-width: 50px; max-height: 50px;" />
            </a>"""
        )
    return "-"

get_profile_avatar.short_description = _("Avatar preview [ 50px ]")

class UserProfileResource(resources.ModelResource):

    class Meta:
        model = UserProfile
        skip_unchanged = True
        report_skipped = False
        fields = (
            "id",
            "profile_avatar",
            "user",
            "preferred_language",
            "email_2",
            "phone_number_2",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "birthday",
            "age",
            "zip_code",
            "country",
            "region",
            "city",
            "street",
            "home_number",)
        exclude = ()

class UserProfileAdmin(UserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {"fields": (
            get_profile_avatar,
            "profile_avatar",
            "user",
            "preferred_language",
            "email_2",
            "phone_number_2"
        )}),
        (_("Main info"), {"fields": (
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "birthday",
            "age",
        )}),
        (_("Geography info"), {"fields": (
            "zip_code",
            "country",
            "region",
            "city",
            "street",
            "home_number",
        )}),
        (_("Important dates"), {"fields": (
            "created_at_datetime",
            "updated_at_datetime",
        )}),
    )
    add_fieldsets = ()
    list_display = ("id", "get_username", "email_2", "phone_number_2", "created_at_datetime", "updated_at_datetime",)
    list_filter = (
        ("user", RelatedDropdownFilter),
        ("country", ChoiceDropdownFilter),
        ("region", DropdownFilter),
        ("city", DropdownFilter),
        ('created_at_datetime', DateTimeRangeFilter),
        ('updated_at_datetime', DateTimeRangeFilter),
    )
    search_fields = ("user__username", "email_2", "phone_number_2", "zip_code",)
    readonly_fields = ("created_at_datetime", "updated_at_datetime", get_profile_avatar,)
    ordering = ("-created_at_datetime", "-updated_at_datetime",)
    filter_horizontal = ()

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return '-'

    get_username.short_description = _("username")

    def save_model(self, request, obj, form, change):
        super(UserProfileAdmin, self).save_model(request, obj, form, change)

    resource_class = UserProfileResource



class UserProfileFilesResource(resources.ModelResource):

    class Meta:
        model = UserProfileFiles
        skip_unchanged = True
        report_skipped = False
        fields = (
            "id",
            "user_profile",
            "user_files",)
        exclude = ('',)

class UserProfileFilesAdmin(ImportExportModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "user_profile",
            "user_files",
        )}),
        (_("Important dates"), {"fields": (
            "created_at_datetime",
            "updated_at_datetime",
        )}),
    )
    add_fieldsets = ("user_profile", "user_files",)
    list_display = (
        "id",
        "get_filename",
        "get_username",
        "created_at_datetime",
        "updated_at_datetime",
    )
    list_filter = (
        ("user_profile__user", RelatedDropdownFilter),
        ('created_at_datetime', DateTimeRangeFilter),
        ('updated_at_datetime', DateTimeRangeFilter),
    )
    search_fields = ()
    readonly_fields = ("created_at_datetime", "updated_at_datetime", )
    ordering = ("-created_at_datetime", "-updated_at_datetime",)
    filter_horizontal = ()

    def get_username(self, obj):
        if obj.user_profile:
            if obj.user_profile.user:
                return obj.user_profile.user.username
        return '-'
    get_username.short_description = _("username")

    def get_filename(self, obj):
        return os.path.basename(obj.user_files.name)
    get_filename.short_description = _("filename")

    def save_model(self, request, obj, form, change):
        super(UserProfileFilesAdmin, self).save_model(request, obj, form, change)

    resource_class = UserProfileFilesResource



class SessionAdmin(admin.ModelAdmin):
    list_display = ['get_session_user_details', 'session_key', '_session_data', 'expire_date']

    def _session_data(self, obj):
        return obj.get_decoded()

    def get_session_user_details(self, obj):
        user_id = obj.get_decoded().get('_auth_user_id')
        user = User.objects.filter(pk=user_id).first()
        if user:
            return "(id : " + str(user.id) + ", name: " + user.username + ")"
        return "(id: -, name: anonymous)"
    get_session_user_details.short_description = _("session user details")



class ConnectionRequestsResource(resources.ModelResource):

    class Meta:
        model = ConnectionRequests
        skip_unchanged = True
        report_skipped = False
        fields = ()
        exclude = ('',)

class ConnectionRequestsAdmin(ImportExportModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "request_unique_id",
            "request_unique_id_parent",
            "request_count",
            "request_count_per_minute",
            "request_count_per_hour",
            "request_count_per_day",
            "request_count_per_week",
            "request_get_full_path",
            "request_user_is_anonymous",
            "request_session_key",
            "request_user_id",
        )}),
        (_("User_agent"), {"fields": (
            "request_user_agent_browser_family",
            "request_user_agent_browser_version",
            "request_user_agent_device_family",
            "request_user_agent_device_brand",
            "request_user_agent_device_model",
            "request_user_agent_device_type",
            "request_user_agent_os_family",
            "request_user_agent_os_version_string",
        )}),
        (_("Request type properties"), {"fields": (
            "request_ip",
            "request_method",
            "request_content_type",
            "request_connection_is_secure",
        )}),
        (_("Request Geo location"), {"fields": (
            "request_location_continent_code",
            "request_location_continent_name",
            "request_location_country_code",
            "request_location_country_name",
            "request_location_region",
            "request_location_city",
            "request_location_dma_code",
            "request_location_postal_code",
            "request_location_latitude",
            "request_location_longitude",
            "request_time_zone",
        )}),
        (_("Request ban properties"), {"fields": (
            "request_restrict_object",
            "request_restrict_object_applied_count",
        )}),
        (_("Request dates"), {"fields": (
            "request_user_last_login_year",
            "request_user_last_login_month",
            "request_user_last_login_day",
            "request_user_last_login_hour",
            "request_user_last_login_minute",
        )}),
        (_("Important dates"), {"fields": (
            "updated_per_save",
            "updated_per_minute",
            "updated_per_hour",
            "updated_per_day",
            "updated_per_week",
            "created_at_datetime",
            "updated_at_datetime",
        )}),
    )
    #add_fieldsets = ("user_profile", "user_files",)
    list_display = (
        "id",
        "get_request_unique_id_shor_name",
        "get_request_unique_id_parent_shor_name",
        "request_count",
        "request_count_per_minute",
        "request_count_per_hour",
        "request_count_per_day",
        "request_count_per_week",
        "request_ip",
        "request_method",
        "request_user_is_anonymous",
        "request_get_full_path",
        "created_at_datetime",
        "updated_at_datetime",
    )
    list_filter = (
        "request_user_is_anonymous",
        "request_user_is_authenticated",
        # ("request_unique_id_parent", RelatedDropdownFilter),
        # ("request_ban", RelatedDropdownFilter),
        ("request_method", DropdownFilter),
        ("request_content_type", DropdownFilter),
        ('created_at_datetime', DateTimeRangeFilter),
        ('updated_at_datetime', DateTimeRangeFilter),
    )
    search_fields = (
            "request_unique_id",
            "request_ip",
            "request_get_full_path",
            "request_session_key",
            "request_user_id",
            "request_user_agent_browser_family",
            "request_user_agent_browser_version",
            "request_user_agent_device_family",
            "request_user_agent_device_brand",
            "request_user_agent_device_model",
            "request_user_agent_device_type",
            "request_user_agent_os_family",
            "request_user_agent_os_version_string",
    )
    readonly_fields = ("created_at_datetime", "updated_at_datetime", )
    ordering = ("request_ip", "-created_at_datetime", "-updated_at_datetime",)
    filter_horizontal = ()
    list_per_page = 10

    def get_request_unique_id_shor_name(self, obj):
        if obj.request_unique_id:
            return '...' + obj.request_unique_id[-23:]
        return '-'
    get_request_unique_id_shor_name.short_description = _("request_unique_id short name")

    def get_request_unique_id_parent_shor_name(self, obj):
        if obj.request_unique_id_parent:
            return obj.request_unique_id_parent.__str__()[:35] + '...' + obj.request_unique_id_parent.__str__()[70:76]
        return '-'
    get_request_unique_id_parent_shor_name.short_description = _("request_unique_id_parent short name")

    def save_model(self, request, obj, form, change):
        super(ConnectionRequestsAdmin, self).save_model(request, obj, form, change)

    resource_class = ConnectionRequestsResource



class ConnectionRequestsUrlsAndPermissionsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "url",
            "url_include_nested_urls",
            "access_via_users",
            "users_include_anonymous",
            "access_via_roles",
        )}),
        (_("DRF Api actions"), {"fields": (
            "api_actions_can_list",
            "api_actions_can_create",
            "api_actions_can_retrieve",
            "api_actions_can_update",
            "api_actions_can_partial_update",
            "api_actions_can_destroy",
        )}),
        (_("Important dates"), {"fields": (
            "created_at_datetime",
            "updated_at_datetime",
        )}),
    )
    list_display = ['id', 'url', 'url_include_nested_urls', 'users_count', 'roles_list']
    list_filter = (
        "users_include_anonymous",
        "url_include_nested_urls",
        "api_actions_can_list",
        "api_actions_can_create",
        "api_actions_can_retrieve",
        "api_actions_can_update",
        "api_actions_can_partial_update",
        "api_actions_can_destroy",
        ('created_at_datetime', DateTimeRangeFilter),
        ('updated_at_datetime', DateTimeRangeFilter),
    )
    search_fields = (
            "url",
    )
    readonly_fields = ("created_at_datetime", "updated_at_datetime", )
    ordering = ("url",)
    filter_horizontal = ('access_via_users', 'access_via_roles',)
    list_per_page = 10

    def users_count(self, obj):
        users_count = ""
        if obj.access_via_users:
            users_count = users_count + str(obj.access_via_users.count()) + " "
        else:
            users_count = users_count + "0 "
        if obj.users_include_anonymous:
            users_count = users_count + "with anonymous"
        return users_count
    users_count.short_description = _("users count")

    def roles_list(self, obj):
        if obj.access_via_roles.count() > 0:
            roles_list = list(obj.access_via_roles.values_list('name', flat=True))
        else:
            roles_list = "-"
        return roles_list
    roles_list.short_description = _("roles list")




admin.site.register(Permission)
admin.site.register(User, UserModelAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfileFiles, UserProfileFilesAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(SessionExtraData)
admin.site.register(ConnectionRequests, ConnectionRequestsAdmin)
admin.site.register(ConnectionRequestsUrlsAndPermissions, ConnectionRequestsUrlsAndPermissionsAdmin)
admin.site.register(ConnectionRequests_BanTemplates)
admin.site.register(ConnectionRequests_BanUsers)
