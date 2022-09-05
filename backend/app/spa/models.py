from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
default_for_app_settings = {
    "app_name": "spa",
    "app_version": 1.0,
    "app_user": {
            "username": "anonymous"
    },
    "app_data": {}
}

class app_settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="spa_app_settings")
    json_data = models.JSONField(null=True, blank=True, default=dict)
    created_at_datetime = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at_datetime = models.DateTimeField(auto_now=True, blank=False)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'spa'
        ordering = ('-created_at_datetime',)

    def save(self, *args, **kwargs):
        if not self.json_data: self.json_data = default_for_app_settings
        if self.user and self.json_data.get("app_user").get("username") == 'anonymous':
            self.json_data["app_user"]["username"] = self.user.username
        super(app_settings, self).save(*args, **kwargs)

    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime: created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime: updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        json_data = "spa_app_settings"
        username = "anonymous"
        if self.user: username = self.user.username

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ username ]: ' + str(username) + ' ' +
            '[ json_data ]: ' + str(json_data) + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )
