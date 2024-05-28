import psycopg2
from config import db_host, db_user_name, db_password, db_name
from logs.loggers import get_logger

_LOGGER = get_logger(__name__)


class DBConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=db_host,
            user=db_user_name,
            password=db_password,
            database=db_name
        )
        self.cursor = self.connection.cursor()
        self.connect_to_schema()
        _LOGGER.info("Корректное подключение к базе данных")

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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
                            login             varchar(50) REFERENCES users(login) UNIQUE, 
                            password          varchar(100) NOT NULL
                            );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS games (
                            login             varchar(50) REFERENCES users(login) UNIQUE,
                            game_count          integer NOT NULL,
                            wins_count			integer NOT NULL
                            );""")
        self.connection.commit()

    def connect_to_schema(self):
        self.cursor.execute("""CREATE SCHEMA IF NOT EXISTS freak_shop;
                            SET SEARCH_PATH = freak_shop;
                            CREATE EXTENSION IF NOT EXISTS pgcrypto;""")
        self.connection.commit()
        self.create_if_not_exists_all_tables()

    def add_user(self, _user_login: str, _user_name: str, _password_1: str, _password_2: str) -> int:
        try:
            if 0 in (len(_user_login), len(_user_name), len(_password_1), len(_password_2)):
                return 11
            self.cursor.execute(f"SELECT * FROM users WHERE login = '{_user_login}'")
            self.connection.commit()
            row = self.cursor.fetchone()
            if row is not None:
                return 12
            if _password_1 != _password_2:
                return 13
            self.cursor.execute(f"INSERT INTO users (login, name) VALUES ('{_user_login}', '{_user_name}');")
            self.cursor.execute(
                f"INSERT INTO passwords (login, password) VALUES ('{_user_login}', crypt('{_password_1}', gen_salt('bf')));")
            self.cursor.execute(f"INSERT INTO games (login, game_count, wins_count) VALUES ('{_user_login}', 0, 0);")
            self.connection.commit()
            return 0
        except Exception as e:
            _LOGGER.error(f'Error while adding user. Exception: {e}')
            return 10

    def check_password(self, _user_login: str, _password: str) -> int:
        self.cursor.execute(f"""SELECT (password = crypt('{_password}', password))
                            AS password_match
                            FROM passwords
                            WHERE login= '{_user_login}';""")
        self.connection.commit()
        row = self.cursor.fetchone()
        if row is None:
            return 16
        if row[0]:
            return 0
        return 14

    def get_all_users(self) -> list[tuple]:
        self.cursor.execute(f"SELECT * FROM users;")
        self.connection.commit()
        return self.cursor.fetchall()

    def get_user_by_login(self, _user_login: str):
        self.cursor.execute(f"SELECT * FROM users WHERE login = '{_user_login}';")
        self.connection.commit()
        row = self.cursor.fetchone()
        if row is None:
            return 16,
        return 0, row[0], row[1], row[2], ""  # id, login, name

    def get_user_by_id(self, _user_id: int):  # status, id, login, name
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = '{_user_id}';")
        row = self.cursor.fetchone()
        if row is None:
            return 15,
        return 0, row[0], row[1], row[2]  # id, login, name

    def login_user(self, _user_login: str, _password: str):
        result = self.check_password(_user_login=_user_login, _password=_password)
        if result != 0:
            return result,
        return self.get_user_by_login(_user_login=_user_login)

    def finish_game(self, _user_login: str, is_winner: bool):
        plus = 1 if is_winner else 0
        self.cursor.execute(f"""UPDATE games
                                SET game_count = game_count + 1, wins_count = wins_count + {plus}
                                WHERE login = '{_user_login}';""")
        self.connection.commit()
        return 0

    def get_best_player(self, count: int = 2) -> list[tuple]:  # list[tuple(name, game_count, game_win)]
        self.cursor.execute(f"""SELECT *
                                FROM games
                                ORDER BY wins_count DESC
                                LIMIT {count};""")
        self.connection.commit()
        return self.cursor.fetchall()

    def close_connection(self) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        _LOGGER.info("Корректное отключение от базы данных")
