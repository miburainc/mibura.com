from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

INSTALLED_APPS += []

MIDDLEWARE += []