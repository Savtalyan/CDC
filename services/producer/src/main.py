from factories.data_factory import DataFactory
from factories.post_factory import PostFactory
from db_conn import Connect


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
    users, _ = DataFactory.generate(1000, 1000)
    real_user_ids = write_users(users)
    posts = PostFactory.create_many(real_user_ids, 1000)
    write_posts(posts)


if __name__ == "__main__":
    main()
