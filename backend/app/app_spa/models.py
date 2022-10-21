from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from app_accounts.models import (
    User,
)


# Create your models here.
default_data_json = {
    "page": {
        "html": [
            [{"lang": "en-US"}],
            [{"head": [
                [{"title": "untitled"}],
                [{"meta": [
                    # do not use close name tag below
                    [{"charset": "utf-8"}],
                    [{"http-equiv": "Content-Type"}, {"content": "text/html; charset=utf-8"}],
                    [{"http-equiv": "X-UA-Compatible"}, {"content": "IE=edge"}],
                    [{"http-equiv": "Pragma"}, {"content": "no-cache"}],
                    [{"name": "viewport"}, {"content": "width=device-width, initial-scale=1.0"}],
                    [{"name": "description"}, {"content": ""}],
                    [{"name": "author"}, {"content": ""}],
                ]}],
                [{"link": [
                    # do not use close name tag below
                    [{"rel": "icon"}, {"type": "image/x-icon"}, {"href": "/static/assets/images/untitled.ico"}],
                    [{"rel": "alternate icon"}, {"type": "image/x-icon"}, {"href": "/static/assets/images/untitled.ico"}],
                    # [{"rel": "stylesheet"}, {"type": "text/css"}, {"href": "/static/spa/css/init.css"}],
                    [{"rel": "stylesheet"}, {"type": "text/css"}, {"href": "/static/spa/css/componentName/componentVersion/index.css"}]
                ]}]
            ]}],
            [{"body": [
                [{"script defer": [
                    # [{"type": "application/javascript"}, {"src": "/static/spa/js/init.js"}],
                    [{"type": "application/javascript"}, {"src": "/static/spa/js/componentName/componentVersion/index.js"}],
                ]}],
            ]}],
        ],
        # is_iframe_page: 1 = True // 0 = False
        "is_iframe_page": 0,
        # is_component_page: 1 = True // 0 = False
        "is_component_page": 0,
        "client_request_block": 0,
        "client_request_debounce": 3000,
        "client_redirect_page": ""
    },
    "data": {

    }
}

class pages_and_urls(models.Model):
    title = models.CharField(blank=False, null=False, default="Page title", max_length=200, verbose_name=_("Page title"))
    url = models.CharField(blank=False, null=False, default="/url_path_example/", max_length=600, verbose_name=_("Page url"))
    # business_logic_python_script = models.CharField(blank=False, null=False, max_length=200, verbose_name=_("Business logic python script"))
    url_version = models.FloatField(blank=True, null=True, default=1.0,
                                              validators=[MinValueValidator(1.0), MaxValueValidator(99.99)],
                                              verbose_name=_('Page version'))
    data_json = models.JSONField(blank=True, null=True, default=dict, verbose_name=_('Page data json'))
    is_actual = models.BooleanField(default=True)
    created_at_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('Record updated at'))

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_spa'
        verbose_name = _('Pages and Urls')
        verbose_name_plural = _('Pages and Urls')
        unique_together = ('url', 'url_version',)
        ordering = ('-created_at_datetime', '-updated_at_datetime')

    def save(self, *args, **kwargs):
        if len(self.url) > 1:
            if self.url[0] != '/': self.url = '/'+self.url
            if self.url[-1] != '/': self.url = '/'+self.url
        if not self.data_json:
            self.data_json = default_data_json
        if self.is_actual:
            pages_and_urls.objects.filter(is_actual=True, url=self.url).exclude(id=self.id).update(is_actual=False)
            users_pages_and_urls.objects.filter(pages_and_urls__url=self.url, pages_and_urls__is_actual=False).update(pages_and_urls=self.id)

        super(pages_and_urls, self).save(*args, **kwargs)

    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime: created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime: updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ title ]: ' + self.title + ' ' +
            '[ url ]: ' + self.url + ' ' +
            '[ url_version ]: ' + str(self.url_version) + ' ' +
            '[ is_actual ]: ' + str(self.is_actual) + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )



class users_pages_and_urls(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=True, related_name="User_UsersPagesAndUrls")
    pages_and_urls = models.ForeignKey(pages_and_urls, on_delete=models.CASCADE, blank=False, null=True, related_name="PagesAndUrls_UsersPagesAndUrls")
    data_json = models.JSONField(blank=True, null=True, default=dict, verbose_name=_('Page data json'))
    created_at_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('Record updated at'))

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_spa'
        verbose_name = _('Users Pages and Urls')
        verbose_name_plural = _('Users Pages and Urls')
        unique_together = ('user', 'pages_and_urls',)
        ordering = ('-created_at_datetime', '-updated_at_datetime')

    def save(self, *args, **kwargs):
        if not self.data_json:
            self.data_json = self.pages_and_urls.data_json
        super(users_pages_and_urls, self).save(*args, **kwargs)

    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime: created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime: updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ username ]: ' + self.user.username + ' ' +
            '[ url ]: ' + self.pages_and_urls.url + ' ' +
            # '[ url_version ]: ' + str(self.url_version) + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )
