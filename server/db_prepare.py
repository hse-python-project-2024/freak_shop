from db_connection import DBConnection

if __name__ == "__main__":
    try:
        db = DBConnection()
        db.drop_and_create_schema()
        print("База данных успешно сброшена. Созданы нужные таблицы")
    except Exception as e:
        print("Ошибка при попытке сбросить базу данных. Попробуйте позже\n", e)
