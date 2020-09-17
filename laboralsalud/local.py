# -*- coding: utf-8 -*-
from .settings import *
from decouple import config

DEBUG = True
# DEBUG = False

DB_USER = "gg"
DB_PASS = "battlehome"
DB_HOST = "127.0.0.1"

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'lbsl',           # Or path to database file if using sqlite3.
            'USER':  DB_USER,    
            'PASSWORD':  DB_PASS,            # Not used with sqlite3.
            'HOST':  DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',      
        },
    }
  
MIDDLEWARE_CLASSES += (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',#Barra DEBUG
)



INSTALLED_APPS += (
    # 'debug_toolbar',    
)