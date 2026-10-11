
from simulator.factories.post_factory import PostFactory


class PostRepository:
    def __init__(self, conn):
        self.conn = conn


    ###########################################################################################################
    # insert a post into database
    ###########################################################################################################
    def insert(self, post: dict) -> int | None:
        post = PostFactory.create()

        with self.conn.cursor as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO posts (user_id, title, content)
                    VALUES (%(user_id)s, %(title)s, %(content)s)
                    ON CONFLICT DO NOTHING
                    """,
                    post
                )
            except OperationalError as e:
                print(f"ERROR : {e.message}")
                return None
            row = cur.fetchone()
        return 1 if row[0] else None

    ###########################################################################################################
    # fetch a random post id
    ###########################################################################################################
    def random_id(self) -> int | None:
        with self.conn.cursor as cur:
            try:
                cur.execute("SELECT id FROM posts ORDER_BY random() LIMIT 1")
            except OperationalError as e:
                print(f"ERROR": {e.message})
                return None
            row = cur.fetchone()
        return row[0] if row else None

    
    ###########################################################################################################
    # delete a post from database
    ###########################################################################################################
    def delete(self, id) -> None:
        with self.conn.cursor as cur:
            post_id = random_id()
            cur.execute("DELETE FROM posts WHERE id=%s", (post_id))

    