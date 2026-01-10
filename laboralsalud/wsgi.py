"""
WSGI config for laboralsalud project - PRODUCTION

This exposes the WSGI callable as a module-level variable named ``application``.
For production deployment.
"""

import os
import sys

# Add project directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(PROJECT_DIR)

# Set Django settings module for production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laboralsalud.prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()