import psycopg2
from config import host, user_name, password, db_name

"""
Если не было схемы от слова совсем, то создаем с пустыми значениями
"""


class DBConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name
        )
        self.cursor = self.connection.cursor()
        self.drop_and_create_schema()
        print("Correct connection to database")

    def drop_and_create_schema(self):
        self.cursor.execute("""DROP SCHEMA IF EXISTS freak_shop CASCADE;
                            CREATE SCHEMA freak_shop;
                            SET SEARCH_PATH = freak_shop;
                            """)
        print("Create schema freak_shop successfully")
        self.cursor.execute("""CREATE TABLE users (
                            user_id           serial PRIMARY KEY,
                            login             varchar(50) NOT NULL,
                            name              varchar(50) NOT NULL
                            );""")
        print("Create table users successfully")

    def add_user(self, user_login: str, user_name: str) -> bool:
        # тут проверка что нет юзера с таким логином
        self.cursor.execute(f"INSERT INTO users (login, name) VALUES ('{user_login}', '{user_name}')")

    def get_all_users(self) -> list[tuple]:
        self.cursor.execute(f"SELECT * FROM users")
        return self.cursor.fetchall()
