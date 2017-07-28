from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

INSTALLED_APPS += []

MIDDLEWARE += []