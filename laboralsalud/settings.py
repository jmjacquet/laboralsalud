# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os,sys
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..') #every dot represent the location of the folder so when you try to delete one dot, the path will be change

SITE_ROOT = PROJECT_ROOT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0pemhta=9#vc5_&1em6_lc04x^(6*(7^qzhns^t$+$mj7!c149'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',  
    'django.contrib.humanize', 
    'localflavor',
    'bootstrap3', 
    'crispy_forms',
    'usuarios',
    'general',
    'entidades',
    'ausentismos',
    'reportes',    
    'fm',
    'modal',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'laboralsalud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, 'templates'),
                ],
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

WSGI_APPLICATION = 'laboralsalud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DB_USER = "jumaja"
DB_PASS = "qwerty"
DB_HOST = "web603.webfaction.com"


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'laboralsalud',           # Or path to database file if using sqlite3.
            'USER':  DB_USER,    
            'PASSWORD':  DB_PASS,            # Not used with sqlite3.
            'HOST':  DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',      
        },
    }

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#             'NAME': 'db.sqlite3',           # Or path to database file if using sqlite3.
#             # 'USER':  DB_USER,    
#             # 'PASSWORD':  DB_PASS,            # Not used with sqlite3.
#             # 'HOST':  DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
#             # 'PORT': '',      
#         },
#     }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TIME_ZONE = 'America/Argentina/Buenos_Aires'
LANGUAGE_CODE = 'es-AR'
SITE_ID = 1
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_L10N = True
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
TIME_INPUT_FORMATS = ('%H:%M',)
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
# STATIC_ROOT = '/home/grupogua/webapps/ironweb/ggcontable/staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, "staticfiles"),   
)

STATICFILES_FINDERS = [
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

ROOT_URL = '/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend','usuarios.authentication.UsuarioBackend',)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = "grupogua"

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'error',} 


CRISPY_TEMPLATE_PACK = 'bootstrap3'           

     