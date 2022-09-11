from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.models import validator_file_size, validator_file_extension
from phonenumber_field.modelfields import PhoneNumberField

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="api_app_settings")
    json_data = models.JSONField(blank=True, null=True, default=dict, verbose_name=_('App json data'))
    use_json_data_version = models.FloatField(blank=True, null=True, default=1.0, validators=[MinValueValidator(1.0), MaxValueValidator(99.99)], verbose_name=_('App json data version'))
    created_at_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_('Record updated at'))

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'api'
        verbose_name = _('API app Settings')
        verbose_name_plural = _('API app Settings')
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



class UserProfile(models.Model):
    GENDER = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    LANGUAGES = (
        ('ru', _('Russian')),
        ('en', _('English')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, unique=True, related_name='UserProfile')
    first_name = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("First Name"))
    middle_name = models.CharField(blank=True, null=True, max_length=100, default="", verbose_name=_("Middle Name"))
    last_name = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Last Name"))
    country = CountryField(blank=True, null=True, verbose_name=_("Country"))
    zip_code = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Zip code'))
    region = models.CharField(blank=True, null=True, max_length=200, verbose_name=_('Region'))
    city = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("City"))
    street = models.CharField(blank=True, null=True, max_length=250, verbose_name=_('Street'))
    home_number = models.CharField(blank=True, null=True, max_length=250)
    gender = models.CharField(blank=True, null=True, max_length=20, choices=GENDER, verbose_name=_('Gender'))
    age = models.IntegerField(blank=True, null=True, default=1, validators=[MinValueValidator(1), MaxValueValidator(150)], verbose_name=_('Age'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    preferred_language = models.CharField(blank=True, null=True, choices=LANGUAGES, max_length=3, default='ENG')
    email_2 = models.EmailField(blank=True, null=True, max_length=233, unique=True, verbose_name=_('Email 2'))
    phone_number_2 = PhoneNumberField(blank=True, null=True, unique=True, db_index=True, verbose_name=_('Phone Number 2'))
    profile_avatar = models.ImageField(blank=True, null=True, default='upload/UserProfile_avatars/default_avatar.png', upload_to='UserProfile_avatars', verbose_name=_('Avatar'))
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=_('Record updated at'))


    def save(self, *args, **kwargs):
        anonymous_profile = UserProfile.objects.filter(user__isnull=True).first()
        if not self.user and anonymous_profile:
            return self
        else:
            super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'api'
        verbose_name = _('User profile')
        verbose_name_plural = _('User profile')
        ordering = ('-created_at_datetime',)

    @property
    def email(self):
        return self.user.email

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name_rus(self):
        return ' '.join(
            (self.first_name, self.middle_name, self.last_name)
        )

    def has_name_rus(self):
        return bool(self.get_full_name_rus().strip())

    def age(self):
        today = date.today()
        born = self.birthday
        rest = 1 if (today.month, today.day) < (born.month, born.day) else 0
        return today.year - born.year - rest
    
    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime: created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime: updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        username = "anonymous"
        if self.user: username = self.user.username

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ username ]: ' + str(username)  + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )

@receiver(post_save, sender=User)
def create_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_UserProfile(sender, instance, **kwargs):
    instance.UserProfile.save()


class UserProfileFiles(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True, related_name="UserProfileFiles")
    user_files = models.FileField(blank=False, null=False, upload_to='UserProfile_files',
                                  validators=[validator_file_size, FileExtensionValidator(allowed_extensions=["txt"])],
                                  help_text=_("Allowed size is 2 MB"), verbose_name=_('User files'))
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=_('Record updated at'))

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'api'
        verbose_name = _('user_UserProfileFiles')
        verbose_name_plural = _('user_UserProfileFiles')
        ordering = ('-created_at_datetime',)

    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime: created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime: updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        username = "anonymous"
        if self.user_profile: username = self.user_profile.user.username

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ username ]: ' + str(username)  + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )
