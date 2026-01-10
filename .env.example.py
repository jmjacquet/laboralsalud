# Service Identification
CONTAINER_NAME=laboralsalud_app
VOLUME_PREFIX=laboral

# Environment Configuration
ENV=production
DEBUG=False

# WSGI Configuration
GUNICORN_WSGI=laboralsalud.wsgi:application
DJANGO_SETTINGS_MODULE=laboralsalud.opal

# Database Configuration
DB_HOST=mariadb_shared
DB_PORT=3306
DB_NAME=lbls
DB_USER=laboral_user
DB_PASS=CHANGE_ME

# Django Settings
SECRET_KEY=CHANGE_ME_MIN_50_CHARS
SESSION_COOKIE_NAME=laboral_session

# Static and Media Paths
STATIC_ROOT=/app/static
MEDIA_ROOT=/app/media

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=CHANGE_ME
EMAIL_PORT=587
SERVER_EMAIL=server@laboralsalud.com.ar
DEFAULT_FROM_EMAIL=noreply@laboralsalud.com.ar

# Gunicorn Configuration
GUNICORN_WORKERS=3
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=60
GUNICORN_BIND=0.0.0.0:8000

# Application Flags
COLLECT_STATIC=false
PYTHONUNBUFFERED=1