import logging
from restaurant_bot.database.db import fetch_all, execute_query
from datetime import datetime

logger = logging.getLogger(__name__)


def get_menu_items(category):
    """Получение списка блюд из указанной категории."""
    try:
        query = """
            SELECT id, name, price, quantity
            FROM menu
            WHERE category = ? AND quantity > 0
        """
        items = fetch_all(query, (category,))
        if not items:
            logger.info(f"Категория '{category}' пуста или не существует.")
        return items
    except Exception as e:
        logger.error(f"Ошибка получения списка блюд для категории '{category}': {e}")
        raise


def add_order(user_id, order_details):
    """Добавление заказа в таблицу orders."""
    try:
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Формат даты ISO
        query = """
            INSERT INTO orders (user_id, order_details, order_date)
            VALUES (?, ?, ?)
        """
        execute_query(query, (user_id, order_details, order_date))
        logger.info(f"Заказ для пользователя {user_id} успешно добавлен.")
        return True
    except Exception as e:
        logger.error(f"Ошибка при добавлении заказа для пользователя {user_id}: {e}")
        raise


def add_to_cart(user_id, item_id):
    """Добавление блюда в корзину пользователя."""
    try:
        query = """
            INSERT INTO cart (user_id, item_id, quantity)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, item_id) 
            DO UPDATE SET quantity = quantity + 1
        """
        execute_query(query, (user_id, item_id))
        logger.info(f"Товар {item_id} добавлен в корзину пользователя {user_id}.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении товара {item_id} в корзину пользователя {user_id}: {e}")
        raise


def view_cart(user_id):
    """Просмотр содержимого корзины пользователя."""
    try:
        query = """
            SELECT menu.name, cart.quantity, menu.price * cart.quantity AS total_price
            FROM cart
            JOIN menu ON cart.item_id = menu.id
            WHERE cart.user_id = ?
        """
        cart_items = fetch_all(query, (user_id,))
        if not cart_items:
            logger.info(f"Корзина пользователя {user_id} пуста.")
        return cart_items
    except Exception as e:
        logger.error(f"Ошибка при получении содержимого корзины пользователя {user_id}: {e}")
        raise


def clear_cart(user_id):
    """Очистка корзины пользователя."""
    try:
        query = "DELETE FROM cart WHERE user_id = ?"
        execute_query(query, (user_id,))
        logger.info(f"Корзина пользователя {user_id} успешно очищена.")
        return True
    except Exception as e:
        logger.error(f"Ошибка при очистке корзины пользователя {user_id}: {e}")
        raise
