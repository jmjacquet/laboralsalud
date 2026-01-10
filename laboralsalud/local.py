# -*- coding: utf-8 -*-
from .settings import *
from decouple import config
import os

DEBUG = config('DEBUG', default="True")

DB_USER = config('DB_USER', default="")
DB_PASS = config('DB_PASS', default="")
DB_HOST = config('DB_HOST', default="")
DB_PORT = config('DB_PORT', default='3306')
DB_NAME = config('DB_NAME', default='lbls')

MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(SITE_ROOT, 'media'))
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(SITE_ROOT, 'static'))
INTERNAL_IPS = ('127.0.0.1', 'localhost',)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    },
}


USE_L10N = False  # Disable localization
DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "d/m/Y H:i"
SHORT_DATE_FORMAT = "d/m/Y"


if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    # Add middleware at the beginning
    MIDDLEWARE = [
                     'debug_toolbar.middleware.DebugToolbarMiddleware',
                 ] + list(MIDDLEWARE)


    # Always show toolbar in DEBUG mode
    def show_toolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
        'INTERCEPT_REDIRECTS': False,
    }

    # INTERNAL_IPS (not strictly needed with SHOW_TOOLBAR_CALLBACK, but good to have)
    INTERNAL_IPS = ['127.0.0.1', 'localhost', '0.0.0.0']

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

