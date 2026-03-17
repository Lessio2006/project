from src.db_connection import Database


def connect_db():
    connection = Database()
    try:
        yield connection
    finally:
        connection.return_connection(connection)



