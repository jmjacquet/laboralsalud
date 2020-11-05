# -*- coding: utf-8 -*-
from .settings import *
from decouple import config

DEBUG = False
# DEBUG = False
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')

STATIC_ROOT = '/home/grupogua/apps/lbsl_static'
MEDIA_ROOT = '/home/grupogua/apps/lbsl_media'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'lbls',           # Or path to database file if using sqlite3.
            'USER':  DB_USER,    
            'PASSWORD':  DB_PASS,            # Not used with sqlite3.
            'HOST':  DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',      
        },
    }

