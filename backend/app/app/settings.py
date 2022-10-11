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
    'app_accounts',
    'app_api',
    'app_spa',
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

############
# SESSIONS #
############

# Age of cookie, in seconds (default: 2 weeks).
SESSION_COOKIE_AGE = 60 * 60 * 1 # 60 * 60 * 24 * 7 * 2
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False
# Whether to set the flag restricting cookie leaks on cross-site requests.
# This can be 'Lax', 'Strict', 'None', or False to disable the flag.
SESSION_COOKIE_SAMESITE = "Lax"
# Whether to save the session data on every request.
SESSION_SAVE_EVERY_REQUEST = False
# Whether a user's session cookie expires when the web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

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
    DATABASES['default'] = dj_database_url.parse(config('APP_DB'))
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
        "OPTIONS": {"min_length": 5},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization & Localization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

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
AUTH_USER_MODEL = 'app_accounts.User'
AUTHENTICATION_BACKENDS = (
    'app_accounts.backends.AuthBackend',
)

FIXTURE_DIRS = (
    BASE_DIR / 'fixtures',
)

ENABLE_SSL = config('ENABLE_SSL', default=False, cast=bool)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
    
SITE_ID = 1

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

#email
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend') #djcelery_email.backends.CeleryEmailBackend #django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = config('EMAIL_HOST', default='smtp.yandex.ru')
EMAIL_PORT = config('EMAIL_PORT', default=465, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='no_reply@dj_zs.me')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='dj_zs12345')
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='no_reply@dj_zs.me')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='dj_zs12345')

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

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    # 'accept',
    # 'accept-encoding',
    # 'authorization',
    "Content-Type",
    # 'dnt',
    # 'origin',
    # 'user-agent',
    'X-CSRFToken',
    # 'x-requested-with',
]

CORS_ORIGIN_WHITELIST = []

if DEBUG:
    CORS_ORIGIN_WHITELIST += ['http://localhost:3000', 'http://localhost:8000', 'https://localhost:3000', 'https://localhost:8000']
else:
    CORS_ORIGIN_WHITELIST += [i for i in config('CORS_ORIGIN_WHITELIST').split(";") if i != '']

CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_AGE =  60 * 60 * 24 * 7 * 52
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
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
from .extra_settings import csp as c_s_p
INSTALLED_APPS += c_s_p.INSTALLED_APPS
MIDDLEWARE += c_s_p.MIDDLEWARE

CSP_DEFAULT_SRC = c_s_p.CSP_DEFAULT_SRC
CSP_STYLE_SRC = c_s_p.CSP_STYLE_SRC
CSP_SCRIPT_SRC = c_s_p.CSP_SCRIPT_SRC
CSP_FONT_SRC = c_s_p.CSP_FONT_SRC
CSP_INCLUDE_NONCE_IN = c_s_p.CSP_INCLUDE_NONCE_IN
CSP_EXCLUDE_URL_PREFIXES = c_s_p.CSP_EXCLUDE_URL_PREFIXES
if DEBUG:
    CSP_WORKER_SRC = ("'self'", "'unsafe-inline'", 'http: blob:', 'https: blob:',)
    CSP_IMG_SRC = ("'self'", "'unsafe-inline'", 'http: data:',  'https: data:',)
else:
    CSP_WORKER_SRC = ("'self'", "'unsafe-inline'", 'https: blob:',)
    CSP_IMG_SRC = ("'self'", "'unsafe-inline'", 'https: data:',)
"""
    django_admin_rangefilter
"""
INSTALLED_APPS += ['rangefilter']
"""
    django_admin_listfilter_dropdown
"""
INSTALLED_APPS += ['django_admin_listfilter_dropdown']
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
SIMPLE_JWT = drf_conf.SIMPLE_JWT
"""
    drf_yasg
"""
from .extra_settings import drf_yasg as dy
INSTALLED_APPS += dy.INSTALLED_APPS
SWAGGER_SETTINGS = dy.SWAGGER_SETTINGS
SWAGGER_SETTINGS['SUPPORTED_SUBMIT_METHODS'] = [i.lower() for i in CORS_ALLOW_METHODS]
"""
    djoser
"""
from .extra_settings import djoser as dj
INSTALLED_APPS += dj.INSTALLED_APPS
DJOSER = dj.DJOSER
"""
    celery
"""
CELERY_BROKER_URL = config('REDIS_URL', default='127.0.0.1:6379')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
"""
    django_user_agents
"""
INSTALLED_APPS += ["django_user_agents"]
"""
    django-geoip2-extras
"""
INSTALLED_APPS += ["geoip2_extras"]
MIDDLEWARE.append("geoip2_extras.middleware.GeoIP2Middleware")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    # required in order for IP addresses to be cached
    "geoip2-extras": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}
GEOIP_PATH = os.path.dirname(__file__)
"""
    django_celery_beat
"""
INSTALLED_APPS += ["django_celery_beat"]
"""
    django_celery_results
"""
INSTALLED_APPS += ["django_celery_results"]
"""
    djcelery_email
"""
INSTALLED_APPS += ["djcelery_email"]
"""
    sentry_sdk
"""
ENABLE_SENTRY = config('ENABLE_SENTRY', default=False, cast=bool)
if ENABLE_SENTRY:
    SENTRY_DSN = config('SENTRY_DSN')
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[DjangoIntegration()]
    )
