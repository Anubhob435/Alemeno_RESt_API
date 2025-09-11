#!/bin/bash
set -e

echo "🚀 Starting Credit Approval System (Option 1: Using existing database)"

# Wait for database to be ready
python simple-wait-for-db.py

# Run migrations (safe to run multiple times)
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "🌟 Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000