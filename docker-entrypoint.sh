#!/bin/bash
set -e

echo "Starting LaboralSalud application..."

# Load .env file if it exists (for local development)
# In production, environment variables should be set by Dokploy
if [ -f /app/.env ]; then
    echo "Loading .env file..."
    export $(cat /app/.env | grep -v '^#' | xargs)
fi

# Wait for database to be ready (if DB_HOST is set)
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-3306}..."
    max_attempts=30
    attempt=0

    while ! nc -z ${DB_HOST} ${DB_PORT:-3306}; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo "ERROR: Database at $DB_HOST:${DB_PORT:-3306} is not available after $max_attempts attempts"
            exit 1
        fi
        echo "Attempt $attempt/$max_attempts: Database not ready, waiting..."
        sleep 2
    done
    echo "Database is ready!"
fi

# Collect static files if needed
if [ "$COLLECT_STATIC" = "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput || true
fi


# Build Gunicorn command with environment variables
GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}
GUNICORN_THREADS=${GUNICORN_THREADS:-2}
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-60}
GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}
GUNICORN_WSGI=${GUNICORN_WSGI:-laboralsalud.wsgi:application}

echo "Starting Gunicorn with:"
echo "  Workers: $GUNICORN_WORKERS"
echo "  Threads: $GUNICORN_THREADS"
echo "  Timeout: $GUNICORN_TIMEOUT"
echo "  Bind: $GUNICORN_BIND"

# If no arguments provided, build gunicorn command
if [ $# -eq 0 ]; then
    exec gunicorn \
        --bind "$GUNICORN_BIND" \
        --workers "$GUNICORN_WORKERS" \
        --threads "$GUNICORN_THREADS" \
        --timeout "$GUNICORN_TIMEOUT" \
        --access-logfile - \
        --error-logfile - \
        "$GUNICORN_WSGI"
else
    # Execute the provided command
    exec "$@"
fi