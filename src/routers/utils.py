import psycopg2 as pg
from src.routers.schemas import UserLoginSchema, OrderSchema
from src.db_connection import Database
from fastapi import HTTPException


def get_id_jwt(info: UserLoginSchema):
    conn = Database().get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SET search_path TO tqm")
            cur.execute("""
            SELECT client_id FROM clients
            WHERE password = %s
            """, (info.password,))

            client_id = cur.fetchone()[0]
            return client_id
    except Exception as e:
        return {"status": HTTPException(status_code=500), "msg": str(e)}
    finally:
        Database.return_connection(conn)


def add_user(user_data: UserLoginSchema):
    Database.initialize()
    conn = Database().get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SET search_path TO tqm")
            cur.execute("""INSERT INTO users (email, password) VALUES (%s, %s)""", (user_data.email, user_data.password))
            conn.commit()
            return {"status": HTTPException(status_code=201), "msg": "User added successfully"}
    except Exception as e:
        return {"status": HTTPException(status_code=500), "msg": str(e)}
    finally:
        Database.return_connection(conn)


def add_order(order_data: OrderSchema):
    Database.initialize()
    conn = Database().get_connection()
    order_amount = order_data.quantity * order_data.price
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO tqm")
            cursor.execute(
                '''INSERT INTO Orders (order_id, clients_id, order_amount, product, quantity) VALUES (%s, %s, %s, %s)''',
                (order_data.order_id, order_data.clients_id, order_amount, order_data.product, order_data.quantity))
            return {'status': 'ok', 'message': 'Order added successfully'}
    except Exception as e:
        return {"status": HTTPException(status_code=500), "msg": str(e)}
    finally:
        Database.return_connection(conn)
