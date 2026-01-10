#!/bin/bash
set -e

echo "Starting LaboralSalud application..."

# Load .env file if it exists (for local development)
if [ -f /app/.env ]; then
    echo "Loading .env file..."
    export $(cat /app/.env | grep -v '^#' | xargs)
fi

# Debug: Show environment variables (for troubleshooting)
echo "=========================================="
echo "Environment Variables Check:"
echo "  ENV=${ENV:-NOT_SET}"
echo "  DEBUG=${DEBUG:-NOT_SET}"
echo "  GUNICORN_WSGI=${GUNICORN_WSGI:-NOT_SET}"
echo "=========================================="

# Determine environment - check multiple ways
# Priority: 1) Explicit GUNICORN_WSGI, 2) ENV variable, 3) DEBUG variable, 4) Default to production
if [ -n "$GUNICORN_WSGI" ]; then
    # Explicit WSGI set, use it
    WSGI_MODULE=$GUNICORN_WSGI
    if [[ "$WSGI_MODULE" == *"wsgi_dev"* ]]; then
        ENV=${ENV:-development}
        DEBUG=${DEBUG:-True}
        echo "Detected DEV mode from GUNICORN_WSGI"
    else
        ENV=${ENV:-production}
        DEBUG=${DEBUG:-False}
        echo "Detected PROD mode from GUNICORN_WSGI"
    fi
else
    # No explicit WSGI, determine from ENV or DEBUG
    ENV=${ENV:-production}
    DEBUG=${DEBUG:-False}

    # Normalize DEBUG value (handle True/true/TRUE/1)
    if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ] || [ "$DEBUG" = "TRUE" ] || [ "$DEBUG" = "1" ]; then
        DEBUG="True"
        ENV="development"
    else
        DEBUG="False"
    fi

    # Check ENV variable
    if [ "$ENV" = "development" ] || [ "$ENV" = "dev" ]; then
        ENV="development"
        DEBUG="True"
    fi
fi

echo "=========================================="
echo "Final Configuration:"
echo "  Environment: $ENV"
echo "  Debug Mode: $DEBUG"
echo "=========================================="

# Wait for database to be ready
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-3306}..."
    max_attempts=30
    attempt=0

    while ! nc -z ${DB_HOST} ${DB_PORT:-3306}; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo "ERROR: Database at $DB_HOST:${DB_PORT:-3306} is not available after $max_attempts attempts"
            echo "Trying to diagnose network issue..."
            echo "Hostname resolution test:"
            getent hosts "$DB_HOST" || echo "  FAILED: Cannot resolve $DB_HOST"
            exit 1
        fi
        echo "Attempt $attempt/$max_attempts: Database not ready, waiting..."
        sleep 2
    done
    echo "✓ Database is ready!"
fi

# Collect static files if needed
if [ "$COLLECT_STATIC" = "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput || true
    echo "✓ Static files collected"
fi

# Run migrations if needed
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput || true
    echo "✓ Migrations completed"
fi

# Determine WSGI file based on environment
if [ "$ENV" = "development" ] || [ "$ENV" = "dev" ]; then
    WSGI_MODULE=${GUNICORN_WSGI:-laboralsalud.wsgi_dev:application}
    echo "Using DEVELOPMENT WSGI (wsgi_dev.py)"
elif [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ] || [ "$DEBUG" = "TRUE" ] || [ "$DEBUG" = "1" ]; then
    WSGI_MODULE=${GUNICORN_WSGI:-laboralsalud.wsgi_dev:application}
    echo "Using DEVELOPMENT WSGI (wsgi_dev.py) - detected from DEBUG=True"
else
    WSGI_MODULE=${GUNICORN_WSGI:-laboralsalud.wsgi:application}
    echo "Using PRODUCTION WSGI (wsgi.py)"
fi

# Override with explicit GUNICORN_WSGI if set (final override)
if [ -n "$GUNICORN_WSGI" ]; then
    WSGI_MODULE=$GUNICORN_WSGI
    echo "Using explicit WSGI override: $WSGI_MODULE"
fi

# Build Gunicorn command with environment variables
GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}
GUNICORN_THREADS=${GUNICORN_THREADS:-2}
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-60}
GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}

echo "=========================================="
echo "Gunicorn Configuration:"
echo "  Workers: $GUNICORN_WORKERS"
echo "  Threads: $GUNICORN_THREADS"
echo "  Timeout: $GUNICORN_TIMEOUT"
echo "  Bind: $GUNICORN_BIND"
echo "  WSGI: $WSGI_MODULE"
echo "=========================================="

# If no arguments provided, build gunicorn command
if [ $# -eq 0 ]; then
    exec gunicorn \
        --bind "$GUNICORN_BIND" \
        --workers "$GUNICORN_WORKERS" \
        --threads "$GUNICORN_THREADS" \
        --timeout "$GUNICORN_TIMEOUT" \
        --access-logfile - \
        --error-logfile - \
        "$WSGI_MODULE"
else
    exec "$@"
fi