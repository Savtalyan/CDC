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

echo "Ensuring debezium_user role exists with correct privileges..."
python3 - <<'PYEOF'
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DEBEZIUM_PASSWORD = "debezium_password"  # keep in sync with register-postgres-connector.json

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'debezium_user'")
if cur.fetchone() is None:
    cur.execute(
        "CREATE ROLE debezium_user WITH LOGIN PASSWORD %s REPLICATION",
        (DEBEZIUM_PASSWORD,),
    )
    print("Created debezium_user.")
else:
    cur.execute(
        "ALTER ROLE debezium_user WITH LOGIN PASSWORD %s REPLICATION",
        (DEBEZIUM_PASSWORD,),
    )
    print("debezium_user already existed - refreshed password/privileges.")

cur.execute(
    sql.SQL("GRANT CONNECT, CREATE ON DATABASE {} TO debezium_user").format(
        sql.Identifier(os.getenv("POSTGRES_DB"))
    )
)
cur.execute("GRANT USAGE ON SCHEMA public TO debezium_user")
# pgoutput requires the connector's user to OWN any table it publishes, not just SELECT on it.
cur.execute("ALTER TABLE public.users OWNER TO debezium_user")
print("Granted privileges and table ownership to debezium_user.")

cur.close()
conn.close()
PYEOF

echo "Waiting for Kafka Connect (Debezium) REST API..."
until curl -s -o /dev/null http://debezium:8083/connectors; do
  echo "Kafka Connect not ready, retrying in 3s..."
  sleep 3
done

echo "Registering/updating Debezium Postgres connector..."
curl -s -X PUT http://debezium:8083/connectors/postgres-cdc-connector/config \
  -H "Content-Type: application/json" \
  -d @/app/register-postgres-connector.json
echo ""

echo "Starting seeder..."
python3 main.py