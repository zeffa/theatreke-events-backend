#!/bin/sh

set e

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn main.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver 0.0.0.0:8000