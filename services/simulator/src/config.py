import os

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environmental variable {name}")
    return value


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=_require("POSTGRES_USER"),
    password=_require("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=_require("POSTGRES_DB"),
)

EVENTS_PER_SEC = float(os.getenv("EVENT_PER_SEC", "2"))
MAX_USERS = int(os.getenv("MAX_USERS_COUNT", "2000"))
MIN_USERS = 50