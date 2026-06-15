from factories.data_factory import DataFactory
from db_conn import Connect


def main():
    users, posts = DataFactory.generate(1000, 1000)
    conn = Connect()
    
    conn.get_env()
    conn.db_name = 'cdc_db'
    conn.connect()

    cur = conn.cursor()

    for user in users:
        cur.execute(
    """
    INSERT INTO users
    (
        u_first_name,
        u_last_name,
        u_email,
        u_phone,
        u_city,
        u_country,
        u_postal
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    """,
    (
        user["u_first_name"],
        user["u_last_name"],
        user["u_email"],
        user["u_phone"],
        user["u_city"],
        user["u_country"],
        user["u_postal"]
    )
    )
    conn.close()

if __name__ == "__main__":
    main()
    