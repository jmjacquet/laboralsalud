# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys
from decouple import config

PROJECT_ROOT = os.path.join(
    os.path.dirname(__file__), ".."
)  # every dot represent the location of the folder so when you try to delete one dot, the path will be change

SITE_ROOT = PROJECT_ROOT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django.contrib.humanize",
    "localflavor",
    "bootstrap3",
    "crispy_forms",
    "general",
    "usuarios",
    "entidades",
    "ausentismos",
    "reportes",
    "modal",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "laboralsalud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
            #     'loaders': [
            #     ('django.template.loaders.cached.Loader', [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #     ]),
            # ],
        },
    },
]

WSGI_APPLICATION = "laboralsalud.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TIME_ZONE = "America/Argentina/Buenos_Aires"
LANGUAGE_CODE = "es-AR"
SITE_ID = 1
USE_I18N = True
USE_THOUSAND_SEPARATOR = False
USE_L10N = True
USE_TZ = True
DEFAULT_CHARSET = "utf-8"
FILE_CHARSET = "utf-8"
TIME_INPUT_FORMATS = ("%H:%M",)
DATE_INPUT_FORMATS = ("%d/%m/%Y",)
# MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = "/media/"
# STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(SITE_ROOT, "staticfiles"),)

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

ROOT_URL = "/"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "usuarios.authentication.UsuarioBackend",
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: "debug",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "error",
}


CRISPY_TEMPLATE_PACK = "bootstrap3"

INTERNAL_IPS = [
    "127.0.0.1",
]


EMAIL_USE_TLS = True
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_PORT = 587

SERVER_EMAIL = config("SERVER_EMAIL")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME")
SECRET_KEY = config("SECRET_KEY")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "logfile": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": os.path.join(SITE_ROOT, "errores.log"),
            "formatter": "verbose",
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "ERROR",
            "filters": ["require_debug_false"],
            # But the emails are plain text by default - HTML is nicer
            "include_html": True,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "testing": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django": {
            "handlers": ["logfile"],
            "level": "INFO",
            "propagate": False,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console', ],
        },
        "general": {
            "handlers": ["logfile"],
            "level": "DEBUG",
            "propagate": False,
        },
        "ausentismos": {
            "handlers": ["logfile"],
            "level": "DEBUG",
            "propagate": False,
        },

    },
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = None