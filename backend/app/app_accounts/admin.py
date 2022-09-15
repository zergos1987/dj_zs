from django.contrib import admin
from import_export import resources
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import (
        User,
        UserProfile,
        UserProfileFiles,
	)



# Register your models here.



admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserProfileFiles)