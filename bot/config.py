import mysql.connector

db_config = {
    'user': 'root',
    'password': '123456789',
    'host': '127.0.0.1',
    'database': 'instapack',
    'raise_on_warnings': True
}
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()


def connect_to_database():
    set_name_query = "SET NAMES 'utf8mb4'"
    set_character_query = "SET CHARACTER SET 'utf8mb4'"
    set_session_collation_connection = "SET SESSION collation_connection = 'utf8mb4_unicode_ci'"
    cursor.execute(set_name_query)
    cursor.execute(set_character_query)
    cursor.execute(set_session_collation_connection)
    cnx.commit()

    cursor.close()
    cnx.close()
