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
import warnings
import shutil
import sqlite3
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = config('APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('APP_DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

# ; - separator of hosts in list
ALLOWED_HOSTS = [i for i in config('APP_ALLOWED_HOSTS').split(";") if i != '']

INTERNAL_IPS = ["127.0.0.1"]


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
    'django.middleware.locale.LocaleMiddleware',
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

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 5},
    }
]

# Internationalization & Localization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

USE_I18N = True

USE_L10N = True

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = (
    BASE_DIR / 'translations/locale',
)

FILE_CHARSET = 'utf-8-sig'


# Time zones
TIME_ZONE = 'Europe/Moscow'
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400

MEDIA_URL = '/upload/'
MEDIA_ROOT = BASE_DIR / 'upload'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / "app/static/",
]


# Other
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = DATE_FORMAT + 'T' + TIME_FORMAT
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%dT%H:%M:%S',     # '2006-10-25T14:30:59'
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
]

FIXTURE_DIRS = (
    BASE_DIR / 'fixtures',
)

ENABLE_SSL = config('ENABLE_SSL', default=False, cast=bool)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/spa/login/'
LOGOUT_REDIRECT_URL = '/spa/login/'
    
SITE_ID = 1

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#########################################################################
##################### EXTRA SETTINGS CONFIG BELOW #######################
#########################################################################
"""
    django_cleanup
"""
INSTALLED_APPS += ["django_cleanup.apps.CleanupConfig"]
"""
    django-cors-headers
"""
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(3, 'corsheaders.middleware.CorsMiddleware')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = []
if DEBUG:
    CORS_ORIGIN_WHITELIST += ['http://localhost:3000', 'http://localhost:8000']
else:
    CORS_ORIGIN_WHITELIST += [i for i in config('CORS_ORIGIN_WHITELIST').split(";") if i != '']
"""
    phonenumber_field
"""
INSTALLED_APPS += ["phonenumber_field"]
"""
    Debug Toolbar
"""
ENABLE_DEBUG_TOOLBAR = config('ENABLE_DEBUG_TOOLBAR', default=False, cast=bool)
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]
    DEBUG_TOOLBAR_CONFIG = {"RESULTS_CACHE_SIZE": 100}
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
if DEBUG:
    CSP_WORKER_SRC = ("'self'", "'unsafe-inline'", 'http: blob:')
    CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'")
    CSP_STYLE_SRC = (
        "'self'", 
        "'unsafe-inline'", 
        'fonts.googleapis.com',
    )
    CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'",)
    CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com')
    CSP_IMG_SRC = ("'self'", "'unsafe-inline'", 'http: data:', 'https: data:')
else:
    CSP_WORKER_SRC = ("'self'", "'unsafe-inline'", 'https: blob:')
    CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'")
    CSP_STYLE_SRC = (
        "'self'", 
        "'unsafe-inline'", 
        'fonts.googleapis.com',
    )
    CSP_SCRIPT_SRC = (
        "'self'", 
        "'unsafe-inline'",
        "https://stackpath.bootstrapcdn.com",
        "https://cdn.jsdelivr.net",
        "https://code.jquery.com",
    )
    CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com')
    CSP_IMG_SRC = ("'self'", "'unsafe-inline'", 'https: data:')
CSP_INCLUDE_NONCE_IN = [
    "script-src"
]
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
"""
    drf_yasg
"""
INSTALLED_APPS += ['drf_yasg']
