#!/bin/bash

python ERPDjangoProject/manage.py makemigrations
python ERPDjangoProject/manage.py migrate

exec "$@"