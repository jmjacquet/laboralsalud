# -*- coding: utf-8 -*-
from .settings import *
from decouple import config

#DEBUG = True
DEBUG = False


DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')


STATIC_ROOT = "/home/lblsl/apps/server_apache/laboralsalud/static/"
MEDIA_ROOT = "/home/lblsl/apps/server_apache/laboralsalud/media/"

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
    
# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',#Barra DEBUG
# )


INSTALLED_APPS += [
     # 'debug_toolbar',       
    'compressor' ,
]

STATICFILES_FINDERS += [
    'compressor.finders.CompressorFinder',
    ]



COMPRESS_ENABLED = False
COMPRESS_OUTPUT_DIR = 'bundles'


COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter','compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]