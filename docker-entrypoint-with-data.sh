#!/bin/bash
set -e

echo "🚀 Starting Credit Approval System (Option 2: With database setup and data ingestion)"

# Wait for database to be ready
python simple-wait-for-db.py

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Ingest data (will skip if data already exists)
echo "📊 Ingesting initial data..."
python manage.py ingest_data

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if specified
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('✅ Superuser created successfully!')
else:
    print('ℹ️  Superuser already exists')
"
fi

# Start the server
echo "🌟 Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000