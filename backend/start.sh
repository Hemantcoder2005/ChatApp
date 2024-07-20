#!/bin/bash

# Update package list and install system dependencies
apt-get update && apt-get install -y libffi-dev libssl-dev

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Daphne server
daphne -b 0.0.0.0 -p $PORT myproject.asgi:application
