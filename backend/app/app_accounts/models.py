from django.db import models
import datetime
# from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, FileExtensionValidator, validate_email, RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.models_validators import validator_file_size, validator_file_extension
from utils.models_file_permissions import (
    CreatePathFor_upload_users_username_files,
    CreatePathFor_upload_users_username_avatars,
)
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from utils.mixins import TimestampMixin
from app_accounts.managers import UserManager
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Group, Permission


# Create your models here.



class User(AbstractBaseUser, PermissionsMixin, TimestampMixin):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'),
                              max_length=255,
                              null=True,
                              blank=True,
                              unique=True,
                              validators=[validate_email]
                              )
    phone = models.CharField(_('phone number'),
                             max_length=17,
                             null=True,
                             blank=True,
                             unique=True,
                             validators=[RegexValidator(
                                 regex=r'^\+?1?\d{9,15}$',
                                 message=_("Phone must be in format: '+19259999999'")
                             )])
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        app_label = 'app_accounts'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('username', 'email', 'phone')



class UserProfile(models.Model):
    GENDER = (
        ('N', _('Not set')),
        ('M', _('Male')),
        ('F', _('Female')),
    )
    LANGUAGES = (
        ('ru', _('Russian')),
        ('en', _('English')),
    )

    profile_avatar = models.ImageField(blank=True, null=True, default='users/default_avatar.png',
                                       upload_to=CreatePathFor_upload_users_username_avatars, verbose_name=_('Avatar'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, unique=True,
                                related_name='UserProfile')
    preferred_language = models.CharField(blank=True, null=True, default='ru', choices=LANGUAGES, max_length=3)
    email_2 = models.EmailField(blank=True, null=True, max_length=233, unique=True, verbose_name=_('Email 2'))
    phone_number_2 = PhoneNumberField(blank=True, null=True, unique=True, db_index=True,
                                      verbose_name=_('Phone Number 2'))
    first_name = models.CharField(blank=True, null=True, max_length=127, verbose_name=_("First Name"))
    middle_name = models.CharField(blank=True, null=True, max_length=127, default="", verbose_name=_("Middle Name"))
    last_name = models.CharField(blank=True, null=True, max_length=127, verbose_name=_("Last Name"))
    gender = models.CharField(blank=True, null=True, default='N', max_length=20, choices=GENDER, verbose_name=_('Gender'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    age = models.IntegerField(blank=True, null=True, default=1,
                              validators=[MinValueValidator(1), MaxValueValidator(150)], verbose_name=_('Age'))
    zip_code = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Zip code'))
    country = CountryField(blank=True, null=True, verbose_name=_("Country"))
    region = models.CharField(blank=True, null=True, max_length=200, verbose_name=_('Region'))
    city = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("City"))
    street = models.CharField(blank=True, null=True, max_length=250, verbose_name=_('Street'))
    home_number = models.CharField(blank=True, null=True, max_length=250)
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    def save(self, *args, **kwargs):
        anonymous_profile = UserProfile.objects.filter(user__isnull=True).first()
        if not self.user and anonymous_profile:
            return self
        else:
            if self.birthday and (not self.age or self.age == 1):
                self.age = round((datetime.date.today() - self.birthday).days/365.25, 0)
            super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Users profile')
        verbose_name_plural = _('Users profile')
        ordering = ('-created_at_datetime',)

    @property
    def get_email(self):
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

    def get_age(self):
        today = datetime.date.today()
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
                '[ username ]: ' + str(username) + ' ' +
                '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
                '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )



class UserProfileFiles(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=False,
                                     related_name="UserProfileFiles")
    user_files = models.FileField(blank=False, null=False, upload_to=CreatePathFor_upload_users_username_files,
                                  validators=[validator_file_size, FileExtensionValidator(allowed_extensions=["txt"])],
                                  help_text=_("Allowed size is 2 MB"), verbose_name=_('User files'))
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Users profile files')
        verbose_name_plural = _('Users profile files')
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
                '[ username ]: ' + str(username) + ' ' +
                '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
                '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )



class ConnectionRequests_BanTemplates(models.Model):
    ban_template_title = models.TextField(blank=True, null=True)
    ban_template_selected_columns = models.TextField(blank=True, null=True)
    limit_contains_request_ip = models.TextField(blank=True, null=True)
    limit_max_request_count = models.IntegerField(blank=False, null=False, default=0,
                              validators=[MinValueValidator(0)])
    limit_max_request_count_per_minute = models.IntegerField(blank=False, null=False, default=0,
                              validators=[MinValueValidator(0)])
    limit_max_request_count_per_hour = models.IntegerField(blank=False, null=False, default=0,
                              validators=[MinValueValidator(0)])
    limit_max_request_count_per_day = models.IntegerField(blank=False, null=False, default=0,
                              validators=[MinValueValidator(0)])
    limit_max_request_count_per_week = models.IntegerField(blank=False, null=False, default=0,
                              validators=[MinValueValidator(0)])
    limit_contains_request_get_full_path = models.TextField(blank=True, null=True)
    limit_boolean_request_user_is_anonymous = models.BooleanField(blank=True, null=True)
    limit_boolean_request_user_is_authenticated = models.BooleanField(blank=True, null=True)
    limit_contains_request_session_key = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_browser_family = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_browser_version = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_device_family = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_device_brand = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_device_model = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_device_type = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_os_family = models.TextField(blank=True, null=True)
    limit_contains_request_user_agent_os_version_string = models.TextField(blank=True, null=True)
    limit_contains_request_content_type = models.TextField(blank=True, null=True)
    limit_boolean_request_connection_is_secure = models.BooleanField(blank=True, null=True)
    limit_contains_request_method = models.TextField(blank=True, null=True)
    limit_contains_request_location_continent_code = models.TextField(blank=True, null=True)
    limit_contains_request_location_continent_name = models.TextField(blank=True, null=True)
    limit_contains_request_location_country_code = models.TextField(blank=True, null=True)
    limit_contains_request_location_country_name = models.TextField(blank=True, null=True)
    limit_contains_request_location_region = models.TextField(blank=True, null=True)
    limit_contains_request_location_city = models.TextField(blank=True, null=True)
    limit_contains_request_location_dma_code = models.TextField(blank=True, null=True)
    limit_contains_request_location_postal_code = models.TextField(blank=True, null=True)
    limit_contains_request_location_latitude = models.TextField(blank=True, null=True)
    limit_contains_request_location_longitude = models.TextField(blank=True, null=True)
    limit_contains_request_time_zone = models.TextField(blank=True, null=True)
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    def save(self, *args, **kwargs):
        self.ban_template_selected_columns = ""
        if self.limit_contains_request_get_full_path is not None and len(self.limit_contains_request_get_full_path) > 0:
            self.ban_template_selected_columns += "limit_contains_request_get_full_path,"
        if self.limit_contains_request_ip is not None and len(self.limit_contains_request_ip) > 0:
            self.ban_template_selected_columns += "limit_contains_request_ip,"
        if self.limit_max_request_count is not None and self.limit_max_request_count > 0:
            self.ban_template_selected_columns += "limit_max_request_count,"
        if self.limit_max_request_count_per_minute is not None and self.limit_max_request_count_per_minute > 0:
            self.ban_template_selected_columns += "limit_max_request_count_per_minute,"
        if self.limit_max_request_count_per_hour is not None and self.limit_max_request_count_per_hour > 0:
            self.ban_template_selected_columns += "limit_max_request_count_per_hour,"
        if self.limit_max_request_count_per_day is not None and self.limit_max_request_count_per_day > 0:
            self.ban_template_selected_columns += "limit_max_request_count_per_day,"
        if self.limit_max_request_count_per_week is not None and self.limit_max_request_count_per_week > 0:
            self.ban_template_selected_columns += "limit_max_request_count_per_week,"
        if self.limit_boolean_request_user_is_anonymous is not None:
            self.ban_template_selected_columns += "limit_boolean_request_user_is_anonymous,"
        if self.limit_boolean_request_user_is_authenticated is not None:
            self.ban_template_selected_columns += "limit_boolean_request_user_is_authenticated,"
        if self.limit_contains_request_session_key is not None and len(self.limit_contains_request_session_key) > 0:
            self.ban_template_selected_columns += "limit_contains_request_session_key,"
        if self.limit_contains_request_user_agent_browser_family is not None and len(self.limit_contains_request_user_agent_browser_family) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_browser_family,"
        if self.limit_contains_request_user_agent_browser_version is not None and len(self.limit_contains_request_user_agent_browser_version) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_browser_version,"
        if self.limit_contains_request_user_agent_device_family is not None and len(self.limit_contains_request_user_agent_device_family) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_device_family,"
        if self.limit_contains_request_user_agent_device_brand is not None and len(self.limit_contains_request_user_agent_device_brand) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_device_brand,"
        if self.limit_contains_request_user_agent_device_model is not None and len(self.limit_contains_request_user_agent_device_model) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_device_model,"
        if self.limit_contains_request_user_agent_device_type is not None and len(self.limit_contains_request_user_agent_device_type) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_device_type,"
        if self.limit_contains_request_user_agent_os_family is not None and len(self.limit_contains_request_user_agent_os_family) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_os_family,"
        if self.limit_contains_request_user_agent_os_version_string is not None and len(self.limit_contains_request_user_agent_os_version_string) > 0:
            self.ban_template_selected_columns += "limit_contains_request_user_agent_os_version_string,"
        if self.limit_contains_request_content_type is not None and len(self.limit_contains_request_content_type) > 0:
            self.ban_template_selected_columns += "limit_contains_request_content_type,"
        if self.limit_contains_request_content_type is not None and len(self.limit_contains_request_content_type) > 0:
            self.ban_template_selected_columns += "limit_contains_request_content_type,"
        if self.limit_boolean_request_connection_is_secure is not None:
            self.ban_template_selected_columns += "limit_boolean_request_connection_is_secure,"
        if self.limit_contains_request_method is not None and len(self.limit_contains_request_method) > 0:
            self.ban_template_selected_columns += "limit_contains_request_method,"
        if self.limit_contains_request_location_continent_code is not None and len(self.limit_contains_request_location_continent_code) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_continent_code,"
        if self.limit_contains_request_location_continent_name is not None and len(self.limit_contains_request_location_continent_name) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_continent_name,"
        if self.limit_contains_request_location_country_code is not None and len(self.limit_contains_request_location_country_code) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_country_code,"
        if self.limit_contains_request_location_country_name is not None and len(self.limit_contains_request_location_country_name) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_country_name,"
        if self.limit_contains_request_location_region is not None and len(self.limit_contains_request_location_region) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_region,"
        if self.limit_contains_request_location_city is not None and len(self.limit_contains_request_location_city) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_city,"
        if self.limit_contains_request_location_dma_code is not None and len(self.limit_contains_request_location_dma_code) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_dma_code,"
        if self.limit_contains_request_location_postal_code is not None and len(self.limit_contains_request_location_postal_code) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_postal_code,"
        if self.limit_contains_request_location_latitude is not None and len(self.limit_contains_request_location_latitude) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_latitude,"
        if self.limit_contains_request_location_longitude is not None and len(self.limit_contains_request_location_longitude) > 0:
            self.ban_template_selected_columns += "limit_contains_request_location_longitude,"
        if self.limit_contains_request_time_zone is not None and len(self.limit_contains_request_time_zone) > 0:
            self.ban_template_selected_columns += "limit_contains_request_time_zone,"
        if len(self.ban_template_selected_columns) > 0:
            self.ban_template_selected_columns = self.ban_template_selected_columns[:-1]
        super(ConnectionRequests_BanTemplates, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Connection requests ban templates')
        verbose_name_plural = _('Connection requests ban templates')
        ordering = ('-created_at_datetime', '-updated_at_datetime',)

    def __str__(self):
        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ ban_template_title ]: ' + str(self.ban_template_title)
        )



class ConnectionRequests_BanUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                      related_name="Users_ConnectionRequestsBans_link_USER")
    template_bans = models.ForeignKey(ConnectionRequests_BanTemplates, on_delete=models.CASCADE, blank=False, null=False,
                      related_name="Users_ConnectionRequestsBans_link_TemplateBans")
    ban_is_permanent = models.BooleanField(blank=False, null=False, default=False)
    ban_minutes = models.IntegerField(blank=True, null=True, default=10)
    ban_message = models.TextField(blank=False, null=False, validators=[MinLengthValidator(10, 'the field must contain at least 10 characters')])
    is_actual = models.BooleanField(blank=False, null=False, default=True)
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    def save(self, *args, **kwargs):
        super(ConnectionRequests_BanUsers, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Connection requests ban users')
        verbose_name_plural = _('Connection requests ban users')
        ordering = ('is_actual', '-created_at_datetime', '-updated_at_datetime',)

    def __str__(self):
        username = "anonymous"
        if self.user:
            username = self.user.username

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ user ]: ' + username + ' ' +
            '[ ban_template_name ]: ' + str(self.template_bans.ban_template_title) + ' ' +
            '[ ban_is_permanent ]: ' + str(self.ban_is_permanent) + ' ' +
            '[ ban_minutes ]: ' + str(self.ban_minutes)
        )



class ConnectionRequests(models.Model):
    request_unique_id = models.CharField(blank=False, null=True, unique=False, max_length=400)
    request_unique_id_parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    request_ip = models.CharField(blank=True, null=True, max_length=200)
    request_count = models.IntegerField(blank=False, null=False, default=1,
                              validators=[MinValueValidator(0)])
    request_count_per_minute = models.IntegerField(blank=False, null=False, default=1,
                              validators=[MinValueValidator(0)])
    request_count_per_hour = models.IntegerField(blank=False, null=False, default=1,
                              validators=[MinValueValidator(0)])
    request_count_per_day = models.IntegerField(blank=False, null=False, default=1,
                              validators=[MinValueValidator(0)])
    request_count_per_week = models.IntegerField(blank=False, null=False, default=1,
                              validators=[MinValueValidator(0)])
    request_get_full_path = models.CharField(blank=True, null=True, max_length=200)
    request_user_is_anonymous = models.BooleanField(blank=False, null=False, default=True)
    request_user_is_authenticated = models.BooleanField(blank=False, null=False, default=False)
    request_session_key = models.CharField(blank=True, null=True, max_length=200)
    request_user_id = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_browser_family = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_browser_version = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_device_family = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_device_brand = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_device_model = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_device_type = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_os_family = models.CharField(blank=True, null=True, max_length=200)
    request_user_agent_os_version_string = models.CharField(blank=True, null=True, max_length=200)
    request_content_type = models.CharField(blank=True, null=True, max_length=200)
    request_connection_is_secure = models.BooleanField(blank=False, null=False, default=False)
    request_method = models.CharField(blank=True, null=True, max_length=200)
    request_user_last_login_year = models.IntegerField(blank=True, null=True)
    request_user_last_login_month = models.IntegerField(blank=True, null=True)
    request_user_last_login_day = models.IntegerField(blank=True, null=True)
    request_user_last_login_hour = models.IntegerField(blank=True, null=True)
    request_user_last_login_minute = models.IntegerField(blank=True, null=True)
    request_location_continent_code = models.CharField(blank=True, null=True, max_length=200)
    request_location_continent_name = models.CharField(blank=True, null=True, max_length=200)
    request_location_country_code = models.CharField(blank=True, null=True, max_length=200)
    request_location_country_name = models.CharField(blank=True, null=True, max_length=200)
    request_location_region = models.CharField(blank=True, null=True, max_length=200)
    request_location_city = models.CharField(blank=True, null=True, max_length=200)
    request_location_dma_code = models.CharField(blank=True, null=True, max_length=200)
    request_location_postal_code = models.CharField(blank=True, null=True, max_length=200)
    request_location_latitude = models.CharField(blank=True, null=True, max_length=200)
    request_location_longitude = models.CharField(blank=True, null=True, max_length=200)
    request_time_zone = models.CharField(blank=True, null=True, max_length=200)
    request_restrict_object = models.JSONField(blank=True, null=True, default=dict, verbose_name=_('Request ban object'))
    request_restrict_object_applied_count = models.IntegerField(blank=False, null=False, default=1,
                              validators=[MinValueValidator(0)])
    updated_per_save = models.DateTimeField(blank=True, null=True, auto_now=False,
                                               verbose_name=_('Updated per save'))
    updated_per_minute = models.DateTimeField(blank=True, null=True, auto_now=False,
                                               verbose_name=_('Updated per mininute'))
    updated_per_hour = models.DateTimeField(blank=True, null=True, auto_now=False,
                                               verbose_name=_('Updated per hour'))
    updated_per_day = models.DateTimeField(blank=True, null=True, auto_now=False,
                                               verbose_name=_('Updated per day'))
    updated_per_week = models.DateTimeField(blank=True, null=True, auto_now=False,
                                               verbose_name=_('Updated per week'))
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    def save(self, save_counters=True, *args, **kwargs):
        if self.updated_at_datetime:
            if not self.updated_per_save:
                self.updated_per_save = self.updated_at_datetime
        if save_counters:
            if self.updated_per_save:
                self.updated_per_save = self.updated_at_datetime
                self.request_count = self.request_count + 1
                if not self.updated_per_minute:
                    self.updated_per_minute = self.updated_per_save
                    self.updated_per_hour = self.updated_per_save
                    self.updated_per_day = self.updated_per_save
                    self.updated_per_week = self.updated_per_save

                time_diff_before_update_at_datetime = (datetime.datetime.now(datetime.timezone.utc) - self.updated_per_minute)
                time_diff_before_interval = (time_diff_before_update_at_datetime.seconds // 60) % 60
                if time_diff_before_interval > 0:
                    self.request_count_per_minute = 1
                    self.updated_per_minute = self.updated_per_save
                else:
                    self.request_count_per_minute += 1

                time_diff_before_update_at_datetime = (datetime.datetime.now(datetime.timezone.utc) - self.updated_per_hour)
                time_diff_before_interval = (time_diff_before_update_at_datetime.seconds // 60 // 60) % 60
                if time_diff_before_interval > 0:
                    self.request_count_per_hour = 1
                    self.updated_per_hour = self.updated_per_save
                else:
                    self.request_count_per_hour += 1

                time_diff_before_update_at_datetime = (datetime.datetime.now(datetime.timezone.utc) - self.updated_per_day)
                time_diff_before_interval = (time_diff_before_update_at_datetime.seconds // 60 // 60 // 24) % 60
                if time_diff_before_interval > 0:
                    self.request_count_per_day = 1
                    self.updated_per_day = self.updated_per_save
                else:
                    self.request_count_per_day += 1

                time_diff_before_update_at_datetime = (datetime.datetime.now(datetime.timezone.utc) - self.updated_per_week)
                time_diff_before_interval = (time_diff_before_update_at_datetime.seconds // 60 // 60 // 24 // 7) % 60
                if time_diff_before_interval > 0:
                    self.request_count_per_week = 1
                    self.updated_per_week = self.updated_per_save
                else:
                    self.request_count_per_week += 1

        max_days_data_hold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
        ConnectionRequests.objects.filter(created_at_datetime__lt=max_days_data_hold).exclude(request_restrict_object__isnull=True).delete()

        super(ConnectionRequests, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Connection requests')
        verbose_name_plural = _('Connection requests')
        ordering = ('request_ip', '-created_at_datetime', '-updated_at_datetime',)

    def __str__(self):
        return (
                '[ id ]: ' + str(self.id) + ' ' +
                '[ request_unique_id ]: ' + str(self.request_unique_id) + ' ' +
                '[ request_ip ]: ' + str(self.request_ip) + ' ' +
                '[ request_get_full_path ]: ' + self.request_get_full_path
        )



class ConnectionRequestsUrlsAndPermissions(models.Model):
    url = models.CharField(blank=False, null=False, default="/", unique=True, max_length=600,
                           validators=[MinLengthValidator(1, 'the field must contain at least 1 character include "/" between')],
                           verbose_name=_("Url"))
    access_via_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="Users_ConnectionRequestsUrls")
    users_include_anonymous = models.BooleanField(blank=False, null=False, default=True)
    access_via_roles = models.ManyToManyField(Group, blank=True, related_name="Roles_ConnectionRequestsUrls")
    url_include_nested_urls = models.BooleanField(blank=False, null=False, default=False)
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    def save(self, *args, **kwargs):
        if len(self.url) == 1:
            if self.url != "/":
                self.url = "/"

        if len(self.url) > 1:
            i = 0
            while i == 0:
                self.url = self.url.replace('//', '/')
                if '//' not in self.url:
                    i += 1

            if self.url[0] == '/':
                self.url = self.url[1:]
            if self.url[-1] != '/':
                self.url = self.url + '/'
        super(ConnectionRequestsUrlsAndPermissions, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Connection requests urls and permissions')
        verbose_name_plural = _('Connection requests urls and permissions')
        ordering = ('-created_at_datetime', '-updated_at_datetime',)

    def __str__(self):
        created_at_datetime = self.created_at_datetime
        if self.created_at_datetime:
            created_at_datetime = self.created_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        updated_at_datetime = self.updated_at_datetime
        if self.updated_at_datetime:
            updated_at_datetime = self.updated_at_datetime.strftime("%m.%d.%Y, %H:%M:%S")
        access_via_users = ""
        if self.access_via_users:
            access_via_users = access_via_users + str(self.access_via_users.count()) + " "
        else:
            access_via_users = access_via_users + "0 "
        access_via_roles = ""
        if self.access_via_roles:
            access_via_roles = access_via_roles + str(self.access_via_roles.count()) + " "
        if self.users_include_anonymous:
            access_via_users = access_via_users + "with anonymous"

        return (
            '[ id ]: ' + str(self.id) + ' ' +
            '[ access_via_users ]: ' + access_via_users + ' ' +
            '[ access_via_roles ]: ' + access_via_roles + ' ' +
            '[ url ]: ' + self.url + ' ' +
            '[ url_include_nested_urls ]: ' + str(self.url_include_nested_urls) + ' ' +
            '[ created_at_datetime ]: ' + str(created_at_datetime) + ' ' +
            '[ updated_at_datetime ]: ' + str(updated_at_datetime)
        )



class SessionExtraData(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, blank=True, null=True, unique=True,
                                related_name='SessionExtraData')
    session_enable = models.BooleanField(blank=False, null=False, default=True)
    session_max_lifetime_minutes = models.IntegerField(blank=False, null=False, default=44640)
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    def get_session_age(self):
        session_age = (datetime.datetime.now(datetime.timezone.utc) - self.created_at_datetime)
        return session_age

    def get_session_user_details(self):
        user_id = self.session.get_decoded().get('_auth_user_id')
        user = User.objects.filter(pk=user_id).first()
        if user:
            user_details = "(id : " + str(user.id) + ", name: " + user.username + ")"
        else:
            user_details = "(id: -, name: anonymous)"
        return user_details

    def save(self, *args, **kwargs):
        if self.created_at_datetime:
            if self.get_session_age() > datetime.timedelta(minutes=self.session_max_lifetime_minutes):
                self.session_enable = False
            if not self.session_enable:
                obj = Session.objects.get(session_key=self.session.session_key)
                obj.delete()
            else:
                super(SessionExtraData, self).save(*args, **kwargs)
        else:
            super(SessionExtraData, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'sessions'
        verbose_name = _('Session extra data')
        verbose_name_plural = _('Session extra data')
        ordering = ('session', '-created_at_datetime',)

    def __str__(self):
        session_valid = (datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE) > self.get_session_age())
        return (
                '[ id ]: ' + str(self.id) + ' ' +
                '[ user_details ]: ' + self.get_session_user_details() + ' ' +
                '[ session_valid ]: ' + str(session_valid) + ' ' +
                '[ session_enable ]: ' + str(self.session_enable) + ' ' +
                '[ session_cookie_age ]: ' + str(datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE)) + ' ' +
                '[ session_age ]: ' + str(self.get_session_age()) + ' ' +
                '[ session_max_lifetime_minutes ]: ' + str(self.session_max_lifetime_minutes) + ' ' +
                '[ created_at_datetime ]: ' + str(self.created_at_datetime) + ' ' +
                '[ session ]: ' + str(self.session.session_key)
        )
    
