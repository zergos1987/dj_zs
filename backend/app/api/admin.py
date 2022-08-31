from django.contrib import admin
from .models import (
        app_settings,
	)



# Register your models here.

class Resource_app_settings(resources.ModelResource):
    class Meta:
        model = app_settings
        skip_unchanged = True
        report_skipped = False
        #fields = ('',)
        #exclude = ('',)


class ModelAdmin_app_settings(ImportExportModelAdmin):
    list_display = [
        field.name for field in app_settings._meta.get_fields() \
        if field.name not in ['M2M_field'] and not field.name.startswith('for_')
    ]
    readonly_fields = ["created_at_datetime", "updated_at_datetime"]
    search_fields = ('user__username',)

    list_filter = (
        ('created_at_datetime', DateRangeFilter),
        ('updated_at_datetime', DateRangeFilter),
    )

    def save_model(self, request, obj, form, change):
        super(ModelAdmin_app_settings, self).save_model(request, obj, form, change)

    def has_import_permission(self, request, obj=None):
        return True

    def has_export_permission(self, request, obj=None):
        return True

    resource_class = Resource_app_settings



admin.site.register(app_settings, ModelAdmin_app_settings)