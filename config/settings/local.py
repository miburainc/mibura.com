from .base import *

DEBUG = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "smtp.office365.com"
EMAIL_HOST_USER = "cs@mibura.com"
EMAIL_HOST_PASSWORD = "^xHpb7S85xE8"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_DEFAULT_FROM = "cs@mibura.com"

SECRET_KEY = 'asjdfhih238r7hufhb2873r8723rasbf'

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += [
	"debug_toolbar",
	"sslserver",
]

MIDDLEWARE += [
	"debug_toolbar.middleware.DebugToolbarMiddleware",
]

ALLOWED_HOSTS = ['*',]

# Stripe

PINAX_STRIPE_PUBLIC_KEY = "pk_test_jW4CJTGamhoH2cCxQljIKiwd"
STRIPE_SECRET_KEY = "sk_test_s6OUz394ThtpufTfUCAFJKwN"
PINAX_STRIPE_DEFAULT_PLAN = "dollar-yearly"
PINAX_STRIPE_INVOICE_FROM_EMAIL = "cs@mibura.com"

PLAID_CLIENT_ID = "58eecc444e95b87bc5622ed3"
PLAID_SECRET_KEY = "b61b2681eef11f3770fcbfb689b6da"
PLAID_PUBLIC_KEY = "87d5d9538ea6876052c9f655c91df8"