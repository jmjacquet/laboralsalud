# -*- coding: utf-8 -*-
from .settings import *


DEBUG = False
# DEBUG = False

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

