#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then

    until pg_isready --host=$SQL_HOST --username=$SQL_USER
    do
    echo "Waiting for PostgreSQL..."
    sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files
python manage.py customsuperuser

exec "$@"