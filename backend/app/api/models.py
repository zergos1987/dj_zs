from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
app_data_v1 = {
    "version": 1
}

default_for_app_settings= {
    "app_name": "api",
    "app_user": {
            "username": "anonymous"
    },
    "app_data": app_data_v1
}

class app_settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="api_app_settings")
    json_data = JSONField(null=True, blank=True, default=default_for_app_settings)

    class Meta:
        # app_label helps django to recognize your db
		app_label = 'api'

    def save(self, *args, **kwargs):
        if self.user and self.json_data.get("app_user").get("username") == 'anonymous':
            self.json_data["app_user"]["username"] = self.user.username
        super(app, self).save(*args, **kwargs)

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, '')))
        field_values = ['user', 'settings', ]
        return ' '.join(field_values)