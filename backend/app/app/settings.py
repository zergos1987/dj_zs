"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from decouple import config
import dj_database_url
import os
import shutil
import sqlite3

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('APP_SECRET_KEY', default='django-insecure-j1rs(!$7)ou-uf45*cqe9!ds9pemx!w0omj&zs4vqz^kh$qcyt')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('APP_DEBUG', default=False, cast=bool)

# ; - separator of hosts in list
ALLOWED_HOSTS = [i for i in config('APP_ALLOWED_HOSTS').split(";") if i != '']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'spa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR  / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_ROUTERS = ['app.extra_settings.db_routers.Router']
DATABASES = {}

if DEBUG:
    DATABASES['default'] = dj_database_url.config(default=f'sqlite:///{BASE_DIR}/' + 'development_db.sqlite3')
    DATABASES['test'] = dj_database_url.config(default=f'sqlite:///{BASE_DIR}/' + 'test_development_db.sqlite3')
    if not os.path.exists(f'{BASE_DIR}/test_development_db.sqlite3'):
        conn = None
        conn = sqlite3.connect(f'{BASE_DIR}/test_development_db.sqlite3')
        conn.close()
else:
    DATABASES['default'] = dj_database_url.parse(default=config('APP_DB'))
    DATABASES['test'] = dj_database_url.config(default=f'sqlite:///{BASE_DIR}/' + 'test_production_db.sqlite3')
    if not os.path.exists(f'{BASE_DIR}/test_production_db.sqlite3'):
        conn = None
        conn = sqlite3.connect(f'{BASE_DIR}/test_production_db.sqlite3')
        conn.close()

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

FILE_CHARSET = 'utf-8-sig'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / "static/assets",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#########################################################################
##################### EXTRA SETTINGS  CONFIG BELOW ######################
#########################################################################
"""
    django_sslserver
"""
INSTALLED_APPS += ['sslserver']
"""
    django_filters
"""
INSTALLED_APPS += ['django_filters']
"""
    django_csp
"""
INSTALLED_APPS += ['csp']
MIDDLEWARE += ['csp.middleware.CSPMiddleware']
"""
    django_admin_rangefilter
"""
INSTALLED_APPS += ['rangefilter']
"""
    django_import_export
"""
from .extra_settings import django_import_export as dix_conf
INSTALLED_APPS += dix_conf.INSTALLED_APPS
IMPORT_EXPORT_USE_TRANSACTIONS = dix_conf.IMPORT_EXPORT_USE_TRANSACTIONS
"""
    django_rest_framework
"""
from .extra_settings import django_rest_framework as drf_conf
INSTALLED_APPS += drf_conf.INSTALLED_APPS
REST_FRAMEWORK = drf_conf.REST_FRAMEWORK
if config('APP_USE_PLUGIN_DRF_JWT', default=False, cast=bool):
    pass
