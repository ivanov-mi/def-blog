#!/bin/bash

python manage.py makemigrations authentication
python manage.py makemigrations core
python manage.py migrate

python manage.py runserver 0.0.0.0:8000