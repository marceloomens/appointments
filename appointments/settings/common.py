"""
Django settings for appointments project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'raven.contrib.django.raven_compat',
    # My apps
    'appointments.apps.timeslots',
    'appointments.apps.common',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'appointments.urls'

SITE_ID = 1

WSGI_APPLICATION = 'appointments.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Messages framework

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG     : 'bg-primary',
    message_constants.INFO      : 'bg-info',
    message_constants.SUCCESS   : 'bg-success',
    message_constants.WARNING   : 'bg-warning',
    message_constants.ERROR     : 'bg-danger',
}

# Auth app configuration

AUTH_USER_MODEL = 'common.User'

# Postmark confiruration
POSTMARK_API_KEY    = os.environ['POSTMARK_API_KEY']
POSTMARK_SENDER     = 'appointments@marceloomens.com'
POSTMARK_TEST_MODE  = False

DEFAULT_FROM_EMAIL  = POSTMARK_SENDER
SERVER_EMAIL        = POSTMARK_SENDER

EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

# Raven app configuration

RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
}

# Timeslots app configuration
TIMESLOTS_DATE_FORMAT = '%Y-%m-%d'
TIMESLOTS_TIME_FORMAT = '%H:%M'
