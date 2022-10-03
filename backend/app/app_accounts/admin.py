from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import (
        User,
        UserProfile,
        UserProfileFiles,
	)
from django.utils.translation import gettext_lazy as _



# Register your models here.



class UserResource(resources.ModelResource):
    class Meta:
    	model = User
	skip_unchanged = True
	report_skipped = False
	fields = ('id', 'username', 'email', 'phone',)

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
		"fields": ("username", "password1", "password2"),
	    },
    	),
    )
    list_display = ("username", "email", "phone", "is_staff",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", ("date_joined", DateTimeRangeFilter),)
    search_fields = ("username", "email", "phone",)
    readonly_fields = ("last_login", "date_joined", "updated_at", "created_at",)
    ordering = ("date_joined",)
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
    
    
    
admin.site.register(User, UserModelAdmin)
admin.site.register(UserProfile)
admin.site.register(UserProfileFiles)
