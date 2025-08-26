#!/bin/bash
set -e

cd /app   # ensure we are in project directory

# Wait for Postgres
if [ "$DATABASE_HOST" ]; then
  echo "Waiting for PostgreSQL..."
  until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER"; do
    sleep 2
  done
fi

# Migrate
echo "Running migrations..."
python manage.py migrate

# Collect static
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
fi

# Run server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
