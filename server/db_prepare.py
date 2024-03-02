from db_connection import DBConnection
from logs.loggers import get_logger

if __name__ == "__main__":
    logger = get_logger(__name__)
    try:
        db = DBConnection()
        db.drop_and_create_schema()
        logger.warning("База данных успешно сброшена. Созданы нужные таблицы")
    except Exception as e:
        logger.error(f"Ошибка при попытке сбросить базу данных. Попробуйте позже\n {e}")
