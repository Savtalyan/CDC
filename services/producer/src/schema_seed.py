from db_conn import Connect 
import psycopg2

connection = Connect()
connection.get_env()

connection.db_name = "postgres"
connection.connect()

connection.conn.autocommit = True

cur = connection.cursor()

cur.execute("""
SELECT 1 FROM pg_database WHERE datname = 'cdc_db';
""")

exists = cur.fetchone()

if not exists:
    cur.execute("CREATE DATABASE cdc_db;")
connection.close()



conn = Connect()
conn.db_name="cdc_db"
conn.connect()

cursor = conn.cursor()

cursor.execute(
            """
-- ############## USERS ###################################
CREATE TABLE IF NOT EXISTS users
(
      id                SERIAL PRIMARY KEY
    , u_first_name      VARCHAR(64) NOT NULL
    , u_last_name       VARCHAR(64) NOT NULL
    , u_email           VARCHAR(255) NOT NULL UNIQUE
    , u_phone           VARCHAR(24) NOT NULL UNIQUE
    , u_city            VARCHAR(64) NOT NULL
    , u_country         VARCHAR(64) NOT NULL
    , u_postal          VARCHAR(12) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_email_phone ON users(u_email, u_phone);


-- ############## POSTS ###################################
CREATE TABLE IF NOT EXISTS posts
(
      id                SERIAL PRIMARY KEY
    , user_id           INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
    , title             VARCHAR(255) NOT NULL
    , content           TEXT NOT NULL
    , created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
    , updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);

"""
    )
conn.close()

