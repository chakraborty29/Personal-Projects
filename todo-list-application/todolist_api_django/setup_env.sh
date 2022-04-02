#!/bin/sh

echo DEBUG=0 >> .env
echo SQL_ENGINE=django.db.backends.postgresql >> .env
echo DATABASE=postgres >> .env

echo SECRET_KEY=$SECRET_KEY >> .env
echo SQL_DATABASE=$SQL_DATABASE >> .env
echo SQL_USER=$SQL_USER >> .env
echo SQL_PASSWORD=$SQL_PASSWORD >> .env
echo SQL_HOST=$SQL_HOST >> .env
echo SQL_PORT=$SQL_PORT >> .env
echo EC2_PUBLIC_IP_ADDRESS=$EC2_PUBLIC_IP_ADDRESS >> .env
echo APP_ENV=$APP_ENV >> .env
echo WEB_IMAGE=$IMAGE:web  >> .env
echo NGINX_IMAGE=$IMAGE:nginx  >> .env
echo CI_REGISTRY_USER=$CI_REGISTRY_USER   >> .env
echo CI_JOB_TOKEN=$CI_JOB_TOKEN  >> .env
echo CI_REGISTRY=$CI_REGISTRY  >> .env
echo IMAGE=$CI_REGISTRY/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME >> .env
echo ADMIN_USERNAME=$ADMIN_USERNAME >> .env
echo ADMIN_PASSWORD=$ADMIN_PASSWORD >> .env
echo ADMIN_EMAIL=$ADMIN_EMAIL >> .env
echo ADMIN_FIREBASE_UID=$ADMIN_FIREBASE_UID >> .env
