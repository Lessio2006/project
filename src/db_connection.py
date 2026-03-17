import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv


load_dotenv()


class Database:
    connection_pool = None

    @classmethod
    def initialize(cls):
        """Создаёт пул соединений при старте приложения"""
        try:
            cls.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,
                20,
                host='localhost',
                port=5432,
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            print("Connection pool created successfully")
        except Exception as e:
            print(f"Failed to create connection pool: {e}")
            raise

    @classmethod
    def get_connection(cls):
        """Устанавливает соединение с пулом"""
        return cls.connection_pool.getconn()

    @classmethod
    def return_connection(cls, conn):
        """Возвращает соединение обратно в пул"""
        cls.connection_pool.putconn(conn)

    @classmethod
    def close_all_connections(cls):
        """Закрывает все соединения (при завершении приложения)"""
        if cls.connection_pool:
            cls.connection_pool.closeall()


