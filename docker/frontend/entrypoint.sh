#!/bin/bash
python3 manage.py makemigrations api
python3 manage.py migrate
gunicorn --bind 0.0.0.0:9000 secureuall.wsgi:application --log-level debug
