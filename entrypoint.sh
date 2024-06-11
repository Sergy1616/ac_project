#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_HOST 5432; do
  sleep 0.1
done

echo "PostgreSQL started"
echo "Applying migrations if needed..."
python manage.py migrate --noinput
echo "Loading initial data if needed..."
python manage.py loaddata ac_app_data.json --ignorenonexistent

exec "$@"