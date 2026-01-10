# -*- coding: utf-8 -*-
from .settings import *
from decouple import config
import os

DEBUG = config('DEBUG', default="False")

DB_USER = config('DB_USER', default="")
DB_PASS = config('DB_PASS', default="")
DB_HOST = config('DB_HOST', default="")
DB_PORT = config('DB_PORT', default='3306')
DB_NAME = config('DB_NAME', default='lbls')

# Use environment variables for paths, fallback to defaults
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(SITE_ROOT, 'static'))
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(SITE_ROOT, 'media'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 300,  # Connection pooling
    },
}
