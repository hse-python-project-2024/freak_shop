from db_connection import DBConnection
from logs.loggers import get_logger

if __name__ == "__main__":
    _LOGGER = get_logger(__name__)
    try:
        db = DBConnection()
        db.drop_and_create_schema()
        _LOGGER.warning("База данных успешно сброшена. Созданы нужные таблицы")
    except Exception as e:
        _LOGGER.error(f"Ошибка при попытке сбросить базу данных. Попробуйте позже\n {e}")
