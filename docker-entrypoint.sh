#!/usr/bin/env bash

python manage.py migrate
if [ $DEBUG == "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn -b 0.0.0.0:8000 core.asgi:application -k uvicorn.workers.UvicornWorker
fi
