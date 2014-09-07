"""
Django settings for dropbox_hello project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import socket
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_DIR = DATA_DIR
LOG_DIR = DATA_DIR
SERVER_FQDN = socket.getfqdn()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't_0e*$=o#qxx%5tfs2h*iy9qwrpz^)1f+b4eqh+q^*j$3+zn#-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dropbox_hello',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dropbox_hello.urls'

WSGI_APPLICATION = 'dropbox_hello.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_DIR, 'db.sqlite3'),
    }
}

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)7s %(asctime)s %(module)s %(process)d'
                       ' %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)7s %(message)s'
        },
        'default': {
            'format': ('%(levelname)7s %(asctime)s'
                       ' %(module)s L%(lineno)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'debug': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': 20 * 1024 * 1024,
            'backupCount': 3,
            'formatter': 'default',
        },
    },
    'loggers': {
        'dropbox_hello.debug': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
