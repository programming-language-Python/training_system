#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python -m gunicorn --timeout 1000 --workers 1 --threads 4 --log-level debug --bind 0.0.0.0:8000 config.wsgi:application