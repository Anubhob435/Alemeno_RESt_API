#!/usr/bin/env python
"""
Simple script to wait for database connection
"""
import os
import sys
import time
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alemeno_RESt_API.settings')
django.setup()

from django.db import connection
from django.db.utils import OperationalError

def wait_for_db():
    """Wait for database to be available"""
    max_retries = 30
    retry_count = 0
    
    print("⏳ Waiting for database connection...")
    
    while retry_count < max_retries:
        try:
            # Test database connection
            connection.ensure_connection()
            print("✅ Database connection successful!")
            return True
        except OperationalError as e:
            retry_count += 1
            print(f"⏳ Database not ready, retrying... ({retry_count}/{max_retries})")
            print(f"   Error: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            retry_count += 1
            time.sleep(2)
    
    print("❌ Could not connect to database after 30 attempts")
    return False

if __name__ == "__main__":
    if wait_for_db():
        sys.exit(0)
    else:
        sys.exit(1)