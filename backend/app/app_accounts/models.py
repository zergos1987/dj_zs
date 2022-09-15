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
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from app_accounts.managers import UserManager



# Create your models here.



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True)
    email = models.EmailField(_('email address'),\
        null=True, blank=True)
    phone = models.CharField(_('phone number'), max_length=30,\
        null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    is_verified = models.BooleanField(_('verified'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        app_label = 'app_accounts'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('username', 'email', 'phone')



class UserProfile(models.Model):
    GENDER = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    LANGUAGES = (
        ('ru', _('Russian')),
        ('en', _('English')),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, unique=True,
                                related_name='UserProfile')
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
    age = models.IntegerField(blank=True, null=True, default=1,
                              validators=[MinValueValidator(1), MaxValueValidator(150)], verbose_name=_('Age'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    preferred_language = models.CharField(blank=True, null=True, choices=LANGUAGES, max_length=3, default='ENG')
    email_2 = models.EmailField(blank=True, null=True, max_length=233, unique=True, verbose_name=_('Email 2'))
    phone_number_2 = PhoneNumberField(blank=True, null=True, unique=True, db_index=True,
                                      verbose_name=_('Phone Number 2'))
    profile_avatar = models.ImageField(blank=True, null=True, default='UserProfile_avatars/default_avatar.png',
                                       upload_to='UserProfile_avatars', verbose_name=_('Avatar'))
    created_at_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True,
                                               verbose_name=_('Record created at'))
    updated_at_datetime = models.DateTimeField(blank=True, null=True, auto_now=True,
                                               verbose_name=_('Record updated at'))

    def save(self, *args, **kwargs):
        anonymous_profile = UserProfile.objects.filter(user__isnull=True).first()
        if not self.user and anonymous_profile:
            return self
        else:
            super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_accounts'
        verbose_name = _('Users profile')
        verbose_name_plural = _('Users profile')
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
                '[ username ]: ' + str(username) + ' ' +
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
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="UserProfileFiles")
    user_files = models.FileField(blank=False, null=False, upload_to='UserProfile_files',
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
