"""
Django settings for checkout_bot project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pardbk7%d8%4(%n_xoob#c&!wh$n_0b6l_^49f!jkksatukto6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

LOGIN_URL = '/login/'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'checkout_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'checkout_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'checkout_bot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'

# contain own static files in root folder that will be
# collected from with python manage.py collectstatic command
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TIMEOUT_PAGE_LAODING = 30

LOG_FILE_PATH = os.path.join(LOGS_DIR, 'google_express_parser.log')
LOG_FILE_MAX_BYTES = 1024 * 1024 * 10  # 10mb
LOG_FILE_BACKUP_COUNT = 3

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s:%(lineno)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'google_express_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'mode': 'w',
            'maxBytes': LOG_FILE_MAX_BYTES,
            'backupCount': LOG_FILE_BACKUP_COUNT,
            'formatter': 'standard'
        }
    },
    'loggers': {
        'google_express_logger': {
            'handlers': ['google_express_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

DRIVER_PATH = os.path.join(BASE_DIR, '3dparty', 'chromedriver')

ROWS_ON_PAGE = 10

from settings_local import *
