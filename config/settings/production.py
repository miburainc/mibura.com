from .base import *
import raven

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DB_URL = get_env_variable('DATABASE_URL')

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['mibura', 'localhost' ])
# END SITE CONFIGURATION

INSTALLED_APPS += ['gunicorn', 'raven.contrib.django.raven_compat', ]


# MIDDLEWARE += []


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
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

RAVEN_CONFIG = {
    'dsn': 'https://5fa67b91426e4d0ca77f38be242ed5ce:b12b07d3bc064ba184fc7491ab35bdb2@sentry.io/196861',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}