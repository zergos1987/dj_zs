from django.db import models
from django.utils.translation import gettext_lazy as _

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=_("Record created at"))
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name=_("Record updated at"))

    class Meta:
        abstract = True
