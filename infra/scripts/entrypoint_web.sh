#!/usr/bin/env bash
set -e

cd /app/src

micromamba run -n web python -m django --version >/dev/null

micromamba run -n web python manage.py migrate --noinput
if [ "${DJANGO_COLLECTSTATIC:-0}" = "1" ]; then
  micromamba run -n web python manage.py collectstatic --noinput
fi


exec micromamba run -n web gunicorn config.wsgi:application \
  -b 0.0.0.0:8001 --workers 2 --timeout 120
