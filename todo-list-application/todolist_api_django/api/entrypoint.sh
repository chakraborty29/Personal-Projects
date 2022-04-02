#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then

    until pg_isready --host=$SQL_HOST --username=$SQL_USER; do
        echo "Waiting for PostgreSQL..."
        sleep 1
    done

fi

# python manage.py migrate   
python manage.py collectstatic --no-input --clear

exec "$@"