"""
Django settings for mibura_new project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = environ.Path(__file__) - 3  # (availlist/config/settings/base.py - 3 = availlist/)

# Load operating system environment variables and then prepare to use them
env = environ.Env()


# Environment variables
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """ Get the environment variable or return exception. """
    try:
        return os.environ[var_name]
    except KeyError:
        error_message = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_message)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Libraries
    'rest_framework',
    'pinax.stripe',
    'cloudinary',
    'corsheaders',
    'crispy_forms',

    # Apps
    'bootcamp',
    'company',
    'datacenter',
    'staffing',
    'support',
    'freshbooks',
    'dynamicscrm',
]

# CORS

CORS_ORIGIN_WHITELIST = (
    'localhost',
    '127.0.0.1',
    '.herokuapp.com',
)

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = (
    'localhost',
    '127.0.0.1',
    '.herokuapp.com',
)

# REST API

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'PAGE_SIZE': 10
}

# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.static',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# FORMS

TASK_UPLOAD_FILE_TYPES = [
    'application/x-iwork-pages-sffpages',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.oasis.opendocument.text',
    'application/pdf',
    'application/rtf'
]
TASK_UPLOAD_FILE_MAX_SIZE = 5242880

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Freshbooks
FRESHBOOKS_URL = 'https://mibura.freshbooks.com/api/2.1/xml-in'
FRESHBOOKS_AUTH = '1be9b30df4a59f7eb6b74fdbb82ba8ac'


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(ROOT_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Media Files


MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = '/media/'

# Cloudinary Image and Video CDN

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "mibura", 
  api_key = "615747629617717", 
  api_secret = "jXGIfwrd6FjjzaDBHNnUOOGwIYg" 
)
