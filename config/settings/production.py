from .base import *
import raven, logging

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = get_env_variable('DJANGO_DEBUG')

if DEBUG == "False":
    DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DB_URL = get_env_variable('DATABASE_URL')

AZURE_SQL_DBNAME='postgres'
AZURE_SQL_USER='miburasqluser'# @db-mibura-sql'
AZURE_SQL_HOST='db-mibura-sql.postgres.database.azure.com'
AZURE_SQL_PASSWORD='AZkey123'
AZURE_SQL_PORT=5432
AZURE_SQL_SSL=True

AZURE_SQL_DB = 'postgres://{user}:{password}@{host}:{port}/{dbname}'.format(user=AZURE_SQL_USER, password=AZURE_SQL_PASSWORD, host=AZURE_SQL_HOST, port=AZURE_SQL_PORT, dbname=AZURE_SQL_DBNAME)

DATABASES = {
    'default': env.db('DATABASE_URL', default=AZURE_SQL_DB),
}

# End Azure

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['mibura.herokuapp.com', 'localhost', '127.0.0.1', ])

INSTALLED_APPS += ['gunicorn', 'raven.contrib.django.raven_compat', ]


# MIDDLEWARE += []


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
if not DEBUG:
	SECURE_HSTS_SECONDS = 60
	SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
	    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
	SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
	    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
	SECURE_BROWSER_XSS_FILTER = True
	SESSION_COOKIE_SECURE = True
	SESSION_COOKIE_HTTPONLY = True
	SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
	CSRF_COOKIE_SECURE = True
	CSRF_COOKIE_HTTPONLY = True
	X_FRAME_OPTIONS = 'DENY'


# Logging

# Sentry Configuration
SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', ],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', ],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry', ],
            'propagate': False,
        },
    },
}
SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
    'DSN': SENTRY_DSN
}