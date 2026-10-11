
from simulator.factories.user_factory import UserFactory


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    ###########################################################################################################
    # insert a user into database
    ###########################################################################################################
    def insert(self, user: dict) -> int | None:
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO users (u_first_name, u_last_name, u_email, u_phone, u_city, u_country, u_postal)
                    VALUES (%(u_first_name)s, %(u_last_name)s, %(u_email)s, %(u_phone)s,
                            %(u_city)s, %(u_country)s, %(u_postal)s)
                    ON CONFLICT DO NOTHING
                    RETURNING id
                    """,
                    user,
                )
            except OperationalError as e:
                print(f"ERROR: {e.message}")
                return None
            
            row = cur.fetchone()
        return 1 if row else None 

    ###########################################################################################################
    # delete a user from database
    ###########################################################################################################
    def delete(self, user_id: int) -> None:
        user_id = self.random_id()

        with self.conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM users WHERE id=%s", (user_id))

            except OperationalError as e:
                print(f"ERROR: {e.message}")
                return None
        return 1

    ###########################################################################################################
    # fetch a random user id 
    ###########################################################################################################
    def random_id(self) -> int | None:
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    SELECT id FROM users ORDER_BY random() LIMIT 1
                    """
                )
            except OperationalError as e:
                print(f"ERROR: {e.message}")
                return None

            row = cur.fetchone()
        return row[0] if row else None 
        



