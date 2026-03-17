from src.db_connection import Database
from fastapi import APIRouter
from .schemas import OrderSchema
from .utils import add_order


router = APIRouter()


@router.post("/orders/pay", tags=["Заказ товара 🛒"])
def set_order(order_data: OrderSchema):
    """Оформляет заказ товара
        Создает запись о заказе в системе и инициирует процесс оплаты.
    Args:
        order_data (OrderSchema): Данные заказа, включая:
            - client_id: ID клиента
            - product: наименование товара
            - quantity: количество
            - order_amount: сумма заказа
    Returns:
        dict: Статус операции и сообщение о результате
    Raises:
        HTTPException(400): При некорректных данных заказа
        HTTPException(500): При ошибке сервера базы данных"""
    add_order(order_data)


@router.get("/orders/pay/{order_id}/client/{client_id}", tags=["Заказ товара 🛒"])
def get_order(order_id: int, client_id: int):
    """Получает статус оплаты заказа для конкретного клиента.
    Проверяет текущий статус платежа по идентификатору заказа и клиента.
    Args:
        order_id (int): Уникальный идентификатор заказа в системе
        client_id (int): Уникальный идентификатор клиента
    Returns:
        dict: Хэш тэйбл со статусо и сообщением
    Raises:
        HTTPException(404): Если заказ или клиент не найдены
        HTTPException(500): При ошибке подключения к базе данных"""
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
    """Оформляет возврат товара
    Args: order_id (int): Уникальный идентификатор заказа
    Returns: dict: Хэш тэбл со статусом и сообщением"""
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
def update_comment(column_name: str, ratio_val:int, comment_id: int):
    """Обновляет комментарий пользователя
    Args:
        column_name (str): Имя поля для обновления. Допустимые значения:
        ratio_val (int): - "ratio": оценка товара (например, от 1 до 5)
        comment_id (int): Уникальный идентификатор комментария
    Returns:
        dict: Объект со статусом и сообщением"""
    Database.initialize()
    conn = Database().get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO tqm")
            cursor.execute(f'''UPDATE comments SET {column_name} = %s WHERE comment_id = %s''', (ratio_val, comment_id,))
            return {'status': 'ok', 'message': 'comment updated successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
