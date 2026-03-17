from src.db_connection import Database
from fastapi import APIRouter
import os
from .schemas import OrderSchema
from .utils import add_order


router = APIRouter()


@router.post("/orders/pay", tags=["Заказ товара 🛒"])
def set_order(order_data: OrderSchema):
    """Оформляет заказ товара"""
    add_order(order_data)


@router.get("/orders/pay/{order_id}/client/{client_id}", tags=["Заказ товара 🛒"])
def get_order(order_id: int, client_id: int):
    """Показывает статус оплаты"""
    Database.initialize()
    conn = Database().get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO tqm")
            cursor.execute('''SELECT status FROM payments WHERE order_id = %s AND client_id = %s''', (order_id, client_id,))
        return {'status': 'ok', 'message': 'Order retrieved successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@router.delete("/orders/progress/{order_id}", tags=["Возврат товара ↩️"])
def delete_order(order_id: int):
    Database.initialize()
    conn = Database().get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO tqm")
            cursor.execute('''DELETE FROM comments WHERE order_id = %s''', (order_id,))
            cursor.execute('''DELETE FROM Orders WHERE order_id = %s''', (order_id,))
        return {'status': 'ok', 'message': 'Order deleted successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@router.put("/reviews/{comment_id}", tags=["Отзывы 💬"])
def update_comment(ratio: str, ratio_val:int, comment_id: int):
    Database.initialize()
    conn = Database().get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO tqm")
            cursor.execute(f'''UPDATE comments SET {ratio} = %s WHERE comment_id = %s''', (ratio_val, comment_id,))
            return {'status': 'ok', 'message': 'comment updated successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
