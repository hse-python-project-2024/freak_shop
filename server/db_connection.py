import psycopg2
from config import host, user_name, password, db_name
from typing import Optional


class DBConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name
        )
        self.cursor = self.connection.cursor()
        self.connect_to_schema()
        print("Correct connection to database")

    def drop_and_create_schema(self):
        self.cursor.execute("""DROP SCHEMA IF EXISTS freak_shop CASCADE;
                            CREATE SCHEMA freak_shop;
                            SET SEARCH_PATH = freak_shop;
                            """)
        self.connection.commit()
        self.create_if_not_exists_all_tables()

    def create_if_not_exists_all_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            user_id           serial PRIMARY KEY,
                            login             varchar(50) NOT NULL UNIQUE,
                            name              varchar(50) NOT NULL
                            );""")

    def connect_to_schema(self):
        self.cursor.execute("""CREATE SCHEMA IF NOT EXISTS freak_shop;
                            SET SEARCH_PATH = freak_shop;""")
        self.connection.commit()
        self.create_if_not_exists_all_tables()

    def add_user(self, _user_login: str, _user_name: str) -> bool:
        try:
            self.cursor.execute(f"SELECT * FROM users WHERE login = '{_user_login}'")
            self.connection.commit()
            row = self.cursor.fetchone()
            if row is not None:
                return False
            self.cursor.execute(f"INSERT INTO users (login, name) VALUES ('{_user_login}', '{_user_name}')")
            self.connection.commit()
            return True
        except Exception as e:
            print(f'Error while adding user. Exception: {e}')
            return False

    def get_all_users(self) -> list[tuple]:
        self.cursor.execute(f"SELECT * FROM users")
        self.connection.commit()
        return self.cursor.fetchall()

    def get_id_by_login(self, _user_login: str) -> Optional[int]:
        self.cursor.execute(f"SELECT * FROM users WHERE login = '{_user_login}'")
        self.connection.commit()
        row = self.cursor.fetchone()
        if row is None:
            return None

        return row[0]

    def get_user_by_id(self, _user_id: int) -> Optional[tuple[int, str, str]]:
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = '{_user_id}'")
        row = self.cursor.fetchone()
        if row is None:
            return None
        return row[0], row[1], row[2]  # id, login, name

    def close_connection(self) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
