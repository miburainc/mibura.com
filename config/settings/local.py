from .base import *

SECRET_KEY = 'asjdfhih238r7hufhb2873r8723rasbf'

DEBUG = True


CSRF_COOKIE_SECURE = False


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "smtp.office365.com"
EMAIL_HOST_USER = "cs@mibura.com"
EMAIL_HOST_PASSWORD = "^xHpb7S85xE8"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_DEFAULT_FROM = "cs@mibura.com"



# Freshbooks
FRESHBOOKS_CLIENT_ID = "dd42ecab13e88af59bc13b678d2ecd8affb9f4d3320940b486a427f38abf8949"
FRESHBOOKS_SECRET_KEY = "709d4c1573ae4790bd08fef5b84cfb240d18b420ad7cd556d11f4c4746f68010"
FRESHBOOKS_API_ROOT = "https://api.freshbooks.com/"
FRESHBOOKS_BEARER_URL = "https://my.freshbooks.com/service/auth/oauth/authorize"

FRESHBOOKS_URL = 'https://miburatest.freshbooks.com/api/2.1/xml-in'
FRESHBOOKS_AUTH = '615144c52b95cc94e62ddc65ec86b273'

# Sept 8
# Bearer token
# 284a6d03fd8435356924eced4288f638174b078f98c5ae8527c80795eaeb9ad2
# Refresh token
# 82d3f06a8d7d76d10d01908c6958f5cd4e19e22fe8f5fa0da91a828186ed4202

# FILES

AZURE_ACCOUNT_NAME = 'blobdev01'
AZURE_ACCOUNT_KEY = 'G3IK3KYOrpo5fyq0Z+u1aFJltZO62uL/VryW+A1z74BEDK3nryMuGpNik5DoDIOGOSPgss4ho77Rj8w3NRO1wQ=='
AZURE_CONTAINER = 'dev-cont-01'

# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'


DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Staging Server DB
# Azure

# Uncomment the following lines to connect to staging postgres database on azure

# AZURE_SQL_DBNAME='postgres'
# AZURE_SQL_USER='dbmiburastagingadmin@db-miburastaging-postgresql'
# AZURE_SQL_HOST='db-miburastaging-postgresql.postgres.database.azure.com'
# AZURE_SQL_PASSWORD='deL!ZWa5NL_Cn'
# AZURE_SQL_PORT=5432
# AZURE_SQL_SSL=True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': AZURE_SQL_DBNAME,
#         'USER': AZURE_SQL_USER,
#         'PASSWORD': AZURE_SQL_PASSWORD,
#         'HOST': AZURE_SQL_HOST,
#         'PORT': AZURE_SQL_PORT,
#         # 'OPTIONS': {
#         #     'sslmode': 'require',
#         # },
#     }
# }

#################################################


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