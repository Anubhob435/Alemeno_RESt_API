# Docker Deployment Options

This project provides flexible Docker deployment options to suit different scenarios.

## 🚀 Quick Start Options

### Option 1: Use Existing External Database (Recommended for Production)

**Use Case**: You already have a PostgreSQL database (like Neon) with data.

```bash
# Using the main docker-compose with profiles
docker-compose --profile external-db up --build

# OR using the dedicated compose file
docker-compose -f docker-compose.external-db.yml up --build
```

**Requirements**:
- `.env` file with your database credentials
- Database should already exist with data

**Access**: http://localhost:8000/api/

---

### Option 2: Complete Local Setup with Data Ingestion

**Use Case**: Fresh start with local PostgreSQL database and automatic data ingestion.

```bash
# Using the main docker-compose with profiles
docker-compose --profile local-db up --build

# OR using the dedicated compose file
docker-compose -f docker-compose.local-db.yml up --build
```

**What it includes**:
- Local PostgreSQL database
- Redis for Celery
- Automatic data ingestion from Excel files
- Celery worker for background tasks
- Admin user creation (admin/admin123)

**Access**: http://localhost:8000/api/

---

## 🔧 Advanced Usage

### With Celery Background Tasks

```bash
# Add Celery to any setup
docker-compose --profile local-db --profile celery up --build
```

### Custom Environment Variables

Create a `.env` file:
```env
DEBUG=true
PGHOST=your-db-host
PGUSER=your-username
PGDATABASE=your-database
PGPASSWORD=your-password
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=your-secure-password
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### Production Mode

```bash
# Set production environment
echo "DEBUG=false" >> .env
docker-compose -f docker-compose.external-db.yml up --build -d
```

---

## 📊 What Each Option Does

### Option 1 (External DB):
1. ✅ Connects to existing database
2. ✅ Runs migrations (safe)
3. ✅ Collects static files
4. ✅ Starts server
5. ❌ No data ingestion (assumes data exists)

### Option 2 (Local DB + Data):
1. ✅ Starts PostgreSQL container
2. ✅ Starts Redis container
3. ✅ Runs migrations
4. ✅ Ingests data from Excel files
5. ✅ Creates admin user
6. ✅ Starts Celery worker
7. ✅ Starts server

---

## 🛠️ Troubleshooting

### Database Connection Issues
```bash
# Check database connectivity
docker-compose logs web

# Restart services
docker-compose down && docker-compose up --build
```

### Data Ingestion Issues
```bash
# Check if Excel files exist
ls -la *.xlsx

# Manual data ingestion
docker-compose exec web python manage.py ingest_data
```

### Reset Everything
```bash
# Remove all containers and volumes
docker-compose down -v
docker system prune -f

# Start fresh
docker-compose -f docker-compose.local-db.yml up --build
```

### Test Docker Container
```bash
# Test the running container
python test-docker-api.py

# Expected output:
# ✅ API is ready!
# ✅ Health Check: Status healthy, Database connected
# ✅ Eligibility Check: Working with existing customers
# ✅ View Customer Loans: Active loans displayed
```

---

## 🔍 Health Checks

Visit these endpoints to verify deployment:

- **API Home**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/ (Option 2 only)
- **Health Check**: http://localhost:8000/api/ (shows database status)

---

## 📝 Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Django debug mode | `false` | No |
| `PGHOST` | PostgreSQL host | - | Yes |
| `PGUSER` | PostgreSQL user | - | Yes |
| `PGDATABASE` | PostgreSQL database | - | Yes |
| `PGPASSWORD` | PostgreSQL password | - | Yes |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | - | No |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | - | No |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | - | No |