import logging
import datetime
from restaurant_bot.database.db import execute_query, fetch_all  # Импортируем функции напрямую


logger = logging.getLogger(__name__)

def add_item_to_menu(name: str, price: float):
    query = "INSERT INTO menu (name, price) VALUES (?, ?)"
    execute_query(query, (name, price))
    try:
        execute_query(query, (name, price))
        logger.info(f"Блюдо {name} добавлено в меню.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении блюда в меню: {e}")


def update_item_price(item_id, price):
    """Обновление цены блюда."""
    query = "UPDATE items SET price = ? WHERE id = ?"
    try:
        execute_query(query, (price, item_id))
        logger.info(f"Цена блюда с ID {item_id} обновлена.")
    except Exception as e:
        logger.error(f"Ошибка при обновлении цены блюда: {e}")


def delete_item(item_id):
    """Удаление блюда из таблицы items."""
    query_check = "SELECT id FROM items WHERE id = ?"
    if not fetch_all(query_check, (item_id,)):
        logger.warning(f"Элемент с ID {item_id} не найден.")
        return
    query = "DELETE FROM items WHERE id = ?"
    try:
        execute_query(query, (item_id,))
        logger.info(f"Элемент с ID {item_id} удалён.")
    except Exception as e:
        logger.error(f"Ошибка при удалении блюда: {e}")


def get_orders_for_today():
    """Получение списка заказов за сегодня."""
    today_date = datetime.date.today().isoformat()
    query = """
        SELECT order_id, user_id, items, total_price, created_at
        FROM orders
        WHERE DATE(created_at) = ?
    """
    return fetch_all(query, (today_date,))



def format_orders(orders):
    """Форматирование списка заказов для отображения."""
    formatted = []
    for order in orders:
        order_id, user_id, items, total_price, created_at = order
        formatted.append(
            f"🆔 Заказ №{order_id}\n"
            f"👤 Пользователь: {user_id}\n"
            f"📦 Товары: {items}\n"
            f"💵 Сумма: {total_price}₽\n"
            f"📅 Дата: {created_at}\n"
            f"------------------------"
        )
    return "\n".join(formatted)
