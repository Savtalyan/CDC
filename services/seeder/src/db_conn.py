from dotenv import load_dotenv
import psycopg2
import os


class Connect:
    def __init__(self):
        self.conn = None
        self.db_user = None
        self.db_pass = None
        self.db_host = None
        self.db_port = None
        self.db_name = None

    def get_env(self):
        load_dotenv()

        self.db_name = os.getenv("POSTGRES_DB")
        self.db_user = os.getenv("POSTGRES_USER")
        self.db_pass = os.getenv("POSTGRES_PASSWORD")
        self.db_host = os.getenv("POSTGRES_HOST", "localhost")
        self.db_port = os.getenv("POSTGRES_PORT", "5432")

        missing = [
            var
            for var in ["POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
            if os.getenv(var) is None
        ]

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

    def connect(self):

        if not self.db_name or not self.db_user or not self.db_pass:
            print(
                f"db_name : {self.db_name}, db_user : {self.db_user}, db_pass : {self.db_pass}"
            )
            raise RuntimeError(f"Missing DB params")

        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                host=self.db_host,
                port=self.db_port,
            )
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def cursor(self):
        try:
            return self.conn.cursor()
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def close(self):
        if not self.conn.autocommit:
            self.conn.commit()
        self.conn.close()
