from django.contrib import admin
from import_export import resources
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
        pages_and_urls,
        users_pages_and_urls,
	)



# Register your models here.



class PagesAndUrlsResoruces(resources.ModelResource):
    class Meta:
        model = pages_and_urls
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'title', 'url', 'url_version',
                  'data_json', 'is_actual', 'created_at_datetime', 'updated_at_datetime',)
        exclude = ()


class PagesAndUrlsModelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'url', 'url_version', 'is_actual', 'created_at_datetime', 'updated_at_datetime']
    readonly_fields = ['created_at_datetime', 'updated_at_datetime']
    search_fields = ('title', 'url', )

    list_filter = (
        'url_version',
        'is_actual',
        ('created_at_datetime', DateTimeRangeFilter),
        ('updated_at_datetime', DateTimeRangeFilter),
    )

    def save_model(self, request, obj, form, change):
        super(PagesAndUrlsModelAdmin, self).save_model(request, obj, form, change)

    def has_import_permission(self, request, obj=None):
        return True

    def has_export_permission(self, request, obj=None):
        return True

    resource_class = PagesAndUrlsResoruces



class UsersPagesAndUrlsResoruces(resources.ModelResource):
    class Meta:
        model = users_pages_and_urls
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'user', 'pages_and_urls', 'data_json', 'created_at_datetime', 'updated_at_datetime',)
        exclude = ()


class UsersPagesAndUrlsModelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user', 'get_pages_and_urls_id', 'get_pages_and_urls_title', 'get_pages_and_urls_url',
                    'created_at_datetime', 'updated_at_datetime']
    readonly_fields = ['created_at_datetime', 'updated_at_datetime']
    search_fields = ()

    list_filter = (
        ("user", RelatedDropdownFilter),
        ('created_at_datetime', DateTimeRangeFilter),
        ('updated_at_datetime', DateTimeRangeFilter),
    )

    def get_pages_and_urls_id(self, obj):
        if obj.pages_and_urls:
            return obj.pages_and_urls.id
        return '-'
    get_pages_and_urls_id.short_description = _("page id")

    def get_pages_and_urls_title(self, obj):
        if obj.pages_and_urls:
            return obj.pages_and_urls.title
        return '-'
    get_pages_and_urls_title.short_description = _("page title")

    def get_pages_and_urls_url(self, obj):
        if obj.pages_and_urls:
            return obj.pages_and_urls.url
        return '-'
    get_pages_and_urls_url.short_description = _("page url")

    def save_model(self, request, obj, form, change):
        super(UsersPagesAndUrlsModelAdmin, self).save_model(request, obj, form, change)

    def has_import_permission(self, request, obj=None):
        return True

    def has_export_permission(self, request, obj=None):
        return True

    resource_class = UsersPagesAndUrlsResoruces


admin.site.register(pages_and_urls, PagesAndUrlsModelAdmin)
admin.site.register(users_pages_and_urls, UsersPagesAndUrlsModelAdmin)
