#!/bin/bash

python ERPDjangoProject/manage.py makemigrations
python ERPDjangoProject/manage.py migrate

python ERPDjangoProject/manage.py runserver 0.0.0.0:8000
