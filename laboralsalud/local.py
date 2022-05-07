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
        "NAME": "lbls",  # Or path to database file if using sqlite3.
        "USER": DB_USER,
        "PASSWORD": DB_PASS,  # Not used with sqlite3.
        "HOST": DB_HOST,  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "3306",
    },
}

INSTALLED_APPS += [
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

if DEBUG:
   INTERNAL_IPS = ('127.0.0.1', 'localhost',)

   MIDDLEWARE += [
       "debug_toolbar.middleware.DebugToolbarMiddleware",  # Barra DEBUG
   ]
   INSTALLED_APPS += (
       'debug_toolbar',
   )

   DEBUG_TOOLBAR_PANELS = [
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   ]

   DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
   }