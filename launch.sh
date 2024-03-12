#!/bin/bash
# launch.sh

# Run Tailwind build (assuming this does not need to keep running)
npm run build:tailwind

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
