from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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


# Stripe

PINAX_STRIPE_PUBLIC_KEY = "pk_test_8TjNbehh0cqmd01HFq3DIawx"
PINAX_STRIPE_SECRET_KEY = "sk_test_zq3p8xe6dyIJrJbcomYpY2Ps"
PINAX_STRIPE_DEFAULT_PLAN = "dollar-yearly"
PINAX_STRIPE_INVOICE_FROM_EMAIL = "sales@mibura.com"
