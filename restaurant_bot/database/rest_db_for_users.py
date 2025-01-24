from db import db_connection


@db_connection
def init_db(conn):
    """Инициализация всех таблиц базы данных."""
    cursor = conn.cursor()
    # Таблица меню
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 0
        )
    ''')
    # Таблица корзины
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            user_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_price REAL NOT NULL,
            quantity INTEGER DEFAULT 1
        )
    ''')


@db_connection
def add_menu_item(conn, name, category, price, quantity):
    """Добавление нового блюда в меню."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO menu (name, category, price, quantity) VALUES (?, ?, ?, ?)",
        (name, category, price, quantity),
    )


@db_connection
def get_menu_by_category(conn, category):
    """Получение всех блюд в определенной категории."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, quantity FROM menu WHERE category = ?", (category,))
    return cursor.fetchall()


@db_connection
def add_to_cart(conn, user_id, item_name, item_price, quantity=1):
    """Добавление блюда в корзину пользователя."""
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM menu WHERE name = ?", (item_name,))
    available_quantity = cursor.fetchone()

    if available_quantity and available_quantity[0] >= quantity:
        cursor.execute(
            "INSERT INTO cart (user_id, item_name, item_price, quantity) VALUES (?, ?, ?, ?)",
            (user_id, item_name, item_price, quantity),
        )
        # Обновление количества в меню
        cursor.execute(
            "UPDATE menu SET quantity = quantity - ? WHERE name = ?",
            (quantity, item_name),
        )
    else:
        print(f"Недостаточно товара {item_name} в меню.")


@db_connection
def get_cart(conn, user_id):
    """Получение содержимого корзины пользователя."""
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, item_price, quantity FROM cart WHERE user_id = ?", (user_id,))
    return cursor.fetchall()


@db_connection
def clear_cart(conn, user_id):
    """Очистка корзины пользователя."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    return cursor.rowcount  # Возвращаем количество удаленных записей


@db_connection
def remove_item_from_cart(conn, user_id, item_name):
    """Удаление конкретного блюда из корзины."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = ? AND item_name = ?", (user_id, item_name))
    return cursor.rowcount  # Возвращаем количество удаленных записей
