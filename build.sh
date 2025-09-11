#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Ingest initial data (only if tables are empty)
python manage.py ingest_data

# Collect static files
python manage.py collectstatic --no-input