#!/bin/bash

python ERPDjangoProject/manage.py migrate

exec "$@"