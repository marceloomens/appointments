from .common import *

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

import dj_database_url
DATABASES = {'default':  dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Raven app configuration
INSTALLED_APPS.append('raven.contrib.django.raven_compat')

RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
}

# Static asset configuration
STATIC_ROOT = 'staticfiles'

# Timeslots app configuration
TIMESLOTS_FUTURE = 90