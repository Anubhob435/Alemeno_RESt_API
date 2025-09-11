FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create static directory to prevent warnings
RUN mkdir -p /app/static /app/staticfiles

# Copy entrypoint scripts and wait script
COPY docker-entrypoint.sh /usr/local/bin/
COPY docker-entrypoint-with-data.sh /usr/local/bin/
COPY simple-wait-for-db.py /app/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-with-data.sh

# Expose port
EXPOSE 8000

# Default entrypoint (can be overridden)
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]