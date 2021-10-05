# -*- coding: utf-8 -*-
from .settings import *
from decouple import config

DEBUG = True
# DEBUG = False
# USE_TZ = False
USE_I18N = False
DB_USER = "gg"
DB_PASS = "battlehome"
DB_HOST = "127.0.0.1"

MEDIA_ROOT = os.path.join(SITE_ROOT, "media")
STATIC_ROOT = os.path.join(SITE_ROOT, "static")
INTERNAL_IPS = ('localhost')
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": "lbsl",  # Or path to database file if using sqlite3.
        "USER": DB_USER,
        "PASSWORD": DB_PASS,  # Not used with sqlite3.
        "HOST": DB_HOST,  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "3306",
    },
}

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Barra DEBUG
]


INSTALLED_APPS += [
    "debug_toolbar",
    "compressor",
]

STATICFILES_FINDERS += [
    "compressor.finders.CompressorFinder",
]


COMPRESS_ENABLED = False
COMPRESS_OUTPUT_DIR = "bundles"

COMPRESS_CSS_FILTERS = ["compressor.filters.css_default.CssAbsoluteFilter", "compressor.filters.cssmin.CSSMinFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]


import sys

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
if TESTING:  # Covers regular testing and django-coverage
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",  #
            "NAME": "test.db",  # Ruta al archivo de la base de datos
        }
    }
