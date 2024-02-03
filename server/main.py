from db_connection import DBConnection

if __name__ == "__main__":
    DB = DBConnection()
    # DB.drop_and_create_schema()
    print(DB.get_all_users())
    DB.add_user("gab1k", "Kamil")
    DB.add_user("Pupkin", "Krasava")
    DB.add_user("Pirog", "Nem")
    print(DB.get_all_users())
    DB.close_connection()

