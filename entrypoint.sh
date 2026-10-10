#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Ensuring default admin user exists (admin / 123)..."
python manage.py init_admin

exec "$@"
