#!/bin/bash
NAME="boilerplate"
NUM_WORKERS=3
DJANGO_WSGI_MODULE=app.wsgi
TIMEOUT=300

echo Executing Django tasks.
python manage.py migrate
python manage.py collectstatic --noinput  # Collect static files

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn --bind 0.0.0.0:8080 ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
#   --log-level=debug \
  --log-file=-
