#!/bin/bash

python academy_a_test_task/manage.py makemigrations storage_app
python academy_a_test_task/manage.py migrate
python academy_a_test_task/manage.py createsuperuser --noinput --email admin@admin.dj