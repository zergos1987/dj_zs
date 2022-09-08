from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
default_for_app_settings = {
    "app": {
        "version": 1.0,
        "name": "api"
    },
    "user": {
            "username": "anonymous"
    },
    "data": {}
}

class app_settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="spa_app_settings")
    json_data = models.JSONField(blank=True, null=True, default=dict, verbose_name=_('App json data'))
    use_json_data_version = models.FloatField(blank=True, null=True, default=1.0, validators=[MinValueValidator(1.0), MaxValueValidator(99.99)], verbose_name=_('App json data version'))
    created_at_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('Record updated at'))

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'spa'
        verbose_name = _('SPA app Settings')
        verbose_name_plural = _('SPA app Settings')
        unique_together = ('user', 'json_data', 'use_json_data_version')
        ordering = ('-created_at_datetime',)

    def save(self, *args, **kwargs):
        if not self.json_data: self.json_data = default_for_app_settings
        if self.user and self.json_data.get("user").get("username") == 'anonymous':
            self.json_data["user"]["username"] = self.user.username
        super(app_settings, self).save(*args, **kwargs)

    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime: created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime: updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        json_data = "api_app_settings"
        username = "anonymous"
        if self.user: username = self.user.username

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ username ]: ' + str(username) + ' ' +
            '[ json_data ]: ' + str(json_data) + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )
