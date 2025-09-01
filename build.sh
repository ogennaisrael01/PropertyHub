#!/usr/bin/env bash
# Exit on error
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Move into the Django project folder
cd houseconnect

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate
