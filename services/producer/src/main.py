import os 
import random 
import signal 
import time 

from seeder.factories.user_factory import UserFactory
from seeder.factories.post_factory import PostFactory
from 
# TODO: add activity events factory 
# TODO: add posts factory

RATE=float(os.getenv("EVENT_PER_SEC", "2"))
MAX_USERS=int(os.getenv("MAX_USERS_COUNT", "2000"))

running = True

# SIGTERM handling functoin
def stop(*_):
    global running
    running = False

# receiving termination signal
signal.signal(signal.SIGTERM, stop)


def choose_operation(user_count):
    if (user_count < 50):
        return "insert_user"
    
    fill = user_count / MAX_USERS
    weights = {
        "insert_user"       : 0.10 * (1 - fill),
        "delete_user"       : 0.02 * fill,
        "update_user"       : 0.10,
        "insert_post"       : 0.25,
        "update_post"       : 0.10,
        "activity_event"    : 0.40,
    }

    return random.choice(list(weights), weights=list(weights.values()))[0]

while running:
    operation = choose_operation()
    execute(operation)
    time.sleep(random.expovariate(RATE))


def write_user(user):
    conn = Connect()
    conn.get_env()
    conn.db_name = os.getenv("POSTGRES_DB")
    conn.connect()
    cur = conn.cursor()

    try:
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
        )
    except ConnectionError as e:
        print(f"ERROR: failed to insert a user: {e}")

    conn.close()

def fetch_user():
    conn = Connect()
    conn.get_env()
    conn.db_name = os.getenv("POSTGRES_DB")
    conn.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT * FROM 
            """
        )

def execute(operation: str) -> None:
    match operation:
        case "insert_user":
            insert_user()
        case "delete_user":
            delete_user()
        case "update_user":
            update_user()
        case "insert_post":
            insert_post()
        case "update_post":
            update_post()
        case "activity_event":
            activity_event()
        case _:
            print("Warning: Wrong operation type")


def insert_user() -> None:
    self.users.insert()

def delete_user() -> None:
    self.users.delete()

def update_user() -> None:
    user_id = self.users.random_id()
    if users_id is None:
        return
    fresh = 
    

def insert_post():
    pass

def update_post():
    pass 

def activity_event():
    pass
