from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.sessions.models import Session
from .models import (
        User,
        UserProfile,
        UserProfileFiles,
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
	exclude = ()

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
    list_display = ("id", "username", "email", "phone", "is_active",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", ("date_joined", DateTimeRangeFilter),)
    search_fields = ("username", "email", "phone",)
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
	    "phone_number_2",
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
        ("created_at_datetime", DateTimeRangeFilter),
        ("updated_at_datetime", DateTimeRangeFilter),
    )
    search_fields = ("user__username", "email_2", "phone_number_2", "zip_code",)
    readonly_fields = ("created_at_datetime", "updated_at_datetime", get_profile_avatar,)
    ordering = ("-created_at_datetime", "-updated_at_datetime",)
    filter_horizontal = ()
	
    def get_username(self, obj):
	if obj.user:
	    return obj.user.username
	return "-"
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
        ("created_at_datetime", DateTimeRangeFilter),
        ("updated_at_datetime", DateTimeRangeFilter),
    )
    search_fields = ()
    readonly_fields = ("created_at_datetime", "updated_at_datetime",)
    ordering = ("-created_at_datetime", "-updated_at_datetime",)
    filter_horizontal = ()
	
    def get_username(self, obj):
	if obj.user_profile:
            if obj.user_profile.user:
	        return obj.user_profile.user.username
	return "-"
    get_username.short_description = _("username")
	
    def get_username(self, obj):
	return os.path.basename(obj.user_files.name)
    get_username.short_description = _("filename")

    def save_model(self, request, obj, form, change):
	super(UserProfileFilesAdmin, self).save_model(request, obj, form, change)
    
    resource_class = UserProfileFilesResource



class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
	    


admin.site.register(User, UserModelAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfileFiles, UserProfileFilesAdmin)
admin.site.register(Session, SessionAdmin)
