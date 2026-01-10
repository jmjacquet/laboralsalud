# ============================================
# DATABASE CONFIGURATION
# ============================================
DB_HOST=mariadb
DB_PORT=3306
DB_USER=laboral_user
DB_PASS=CHANGE_ME_IN_DOKPLOY

# ============================================
# DJANGO SETTINGS
# ============================================
SECRET_KEY=CHANGE_ME_IN_DOKPLOY_MIN_50_CHARS
SESSION_COOKIE_NAME=laboral_session
DJANGO_SETTINGS_MODULE=laboralsalud.opal
DEBUG=False

# ============================================
# EMAIL CONFIGURATION
# ============================================
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=CHANGE_ME_IN_DOKPLOY
EMAIL_PORT=587
SERVER_EMAIL=server@laboralsalud.com.ar
DEFAULT_FROM_EMAIL=noreply@laboralsalud.com.ar

# ============================================
# GUNICORN CONFIGURATION
# ============================================
# Number of worker processes
# Recommended: (2 × CPU cores) + 1
# For 2 cores: 5, For 4 cores: 9
GUNICORN_WORKERS=3

# Number of threads per worker
# Recommended: 2-4 threads per worker
GUNICORN_THREADS=2

# Request timeout in seconds
# Increase for long-running requests
GUNICORN_TIMEOUT=60

# Bind address and port
# Format: IP:PORT or just :PORT
GUNICORN_BIND=0.0.0.0:8000

# WSGI application path
# Usually don't need to change this
GUNICORN_WSGI=laboralsalud.wsgi:application

# ============================================
# APPLICATION FLAGS
# ============================================
COLLECT_STATIC=false
RUN_MIGRATIONS=false
PYTHONUNBUFFERED=1