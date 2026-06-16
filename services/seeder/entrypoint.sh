#!/bin/bash
set -e

echo "Waiting for postgres to be ready..."
until python3 -c "
import psycopg2, os
from dotenv import load_dotenv
load_dotenv()
psycopg2.connect(
    dbname='postgres',
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
).close()
" 2>/dev/null; do
  echo "Postgres not ready, retrying in 2s..."
  sleep 2
done

echo "Running db init..."
python3 db_init.py

echo "Starting seeder..."
python3 main.py