#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser --no-input
exec gunicorn api.wsgi:application -b 0.0.0.0:8000 --reload --log-level info
