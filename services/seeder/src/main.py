from factories.data_factory import DataFactory
from factories.post_factory import PostFactory
from db_conn import Connect
import requests 
import time

def init_debezium():
    debezium_url = "http://debezium:8083"
    
    while True:
        try:
            response = requests.get(f"{debezium_url}/")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        print("Waiting for Debezium...")
        time.sleep(5)

    existing = requests.get(f"{debezium_url}/connectors/postgres-connector")
    if existing.status_code == 200:
        print("Connector already registered. Skipping")
        return

    connector_config = {
        "name": "postgres-connector",
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "database.hostname": "postgres",
            "database.port": "5432",
            "database.user": "debezium_user",
            "database.password": "debezium_pass",
            "database.dbname": "cdc_db",
            "topic.prefix": "cdc",
            "plugin.name": "pgoutput",
            "publication.name": "debezium_publication",
            "key.converter": "io.confluent.connect.avro.AvroConverter",
            "key.converter.schema.registry.url": "http://schema-registry:8081",
            "value.converter": "io.confluent.connect.avro.AvroConverter",
            "value.converter.schema.registry.url": "http://schema-registry:8081"
        }
    }

    for attempt in range(10):
        response = requests.post(
            f"{debezium_url}/connectors",
            json=connector_config,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print("Connector registered successfully")
            return
        elif response.status_code == 500 and "cluster" in response.text:
            print(f"Debezium not ready yet (attempt {attempt + 1}/10), retrying...")
            time.sleep(5)
        else:
            raise RuntimeError(f"Failed to register connector: {response.status_code} {response.text}")

    raise RuntimeError("Debezium did not become ready after 10 attempts")

def write_users(users):
    conn = Connect()
    conn.get_env()
    conn.db_name = "cdc_db"
    conn.connect()
    cur = conn.cursor()

    inserted_ids = []
    for user in users:
        cur.execute(
            """
        INSERT INTO users (u_first_name, u_last_name, u_email, u_phone, u_city, u_country, u_postal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
        """,
            (
                user["u_first_name"],
                user["u_last_name"],
                user["u_email"],
                user["u_phone"],
                user["u_city"],
                user["u_country"],
                user["u_postal"],
            ),
        )  # ← closes cur.execute()
        row = cur.fetchone()
        if row:
            inserted_ids.append(row[0])

    conn.close()
    return inserted_ids


def write_posts(posts):
    conn = Connect()
    conn.get_env()
    conn.db_name = "cdc_db"
    conn.connect()
    cur = conn.cursor()

    for post in posts:
        cur.execute(
            """
        INSERT INTO posts (user_id, title, content)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
        """,
            (post["user_id"], post["title"], post["content"]),
        )

    conn.close()


def main():
    init_debezium()
    users, _ = DataFactory.generate(100, 100)
    real_user_ids = write_users(users)
    posts = PostFactory.create_many(real_user_ids, 1001)
    write_posts(posts)


if __name__ == "__main__":
    main()
