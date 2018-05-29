"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from ast import literal_eval as make_tuple

# Django Environ
import environ
root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, True), ALLOWED_HOSTS=(list, []),)  # set default values and casting
environ.Env.read_env(root('.env'))  # reading .env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.sites',
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # apps
    'accounts',
    'cards',
    # libs
    'django_ses',
    'webpack_loader',
    'localflavor',
    'rest_framework',
    'storages',
    'bootstrap4',
    'imagekit',
    'mail_templated',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cards.context.departments',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Whitenoise
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

# Webpack
if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'dev'),
    )

if not DEBUG:
    WEBPACK_LOADER = {
      'DEFAULT': {
          'BUNDLE_DIR_NAME': '/',
          'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats-prod.json'),
      }
    }
else:
    WEBPACK_LOADER = {
      'DEFAULT': {
          'BUNDLE_DIR_NAME': '/',
          'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
          'IGNORE': ['.+\.hot-update.js', '.+\.map'],
          'CACHE': not DEBUG
      }
    }

# Cors
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = make_tuple(env('CORS_ORIGIN_WHITELIST'))

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'UNICODE_JSON': False
}

# User substitution
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = 'accounts.User'

# Login
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/cuenta/login'

# Site
SITE_ID = 1

# Email Configuration
EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# AWS S3
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'app.storages.MediaStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# STATIC_HOST = "https://%s/" % (AWS_S3_CUSTOM_DOMAIN) if not DEBUG else ''
STATIC_URL = '/static/'

# Django-Registration

ACCOUNT_ACTIVATION_DAYS = 14
REGISTRATION_AUTO_LOGIN = True


PROBABILITY_LOW = env('PROBABILITY_LOW')
PROBABILITY_MEDIUM = env('PROBABILITY_MEDIUM')
PROBABILITY_HIGH = env('PROBABILITY_HIGH')
PROBABILITY_SPECIAL = env('PROBABILITY_SPECIAL')
