#!/usr/bin/env python
"""
Simple database connection test without Django setup
"""
import os
import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres():
    """Wait for PostgreSQL to be available"""
    max_retries = 30
    retry_count = 0
    
    # Get database connection details from environment
    host = os.getenv('PGHOST', 'localhost')
    database = os.getenv('PGDATABASE', 'postgres')
    user = os.getenv('PGUSER', 'postgres')
    password = os.getenv('PGPASSWORD', '')
    port = os.getenv('PGPORT', '5432')
    
    print(f"⏳ Waiting for PostgreSQL at {host}:{port}/{database}...")
    
    while retry_count < max_retries:
        try:
            # Try to connect to PostgreSQL
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port,
                connect_timeout=5
            )
            conn.close()
            print("✅ PostgreSQL connection successful!")
            return True
        except OperationalError as e:
            retry_count += 1
            print(f"⏳ PostgreSQL not ready, retrying... ({retry_count}/{max_retries})")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Connection error: {e}")
            retry_count += 1
            time.sleep(2)
    
    print("❌ Could not connect to PostgreSQL after 30 attempts")
    return False

if __name__ == "__main__":
    import sys
    if wait_for_postgres():
        sys.exit(0)
    else:
        sys.exit(1)