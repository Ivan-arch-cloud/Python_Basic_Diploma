import sqlite3
import logging
from restaurant_bot.config_data.config import DB_PATH

logger = logging.getLogger(__name__)

def init_db():
    """Инициализация базы данных и таблиц."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    callback_data TEXT NOT NULL UNIQUE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_callback TEXT NOT NULL,
                    name TEXT NOT NULL,
                    callback_data TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL CHECK(price >= 0) 
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL, 
                    order_details TEXT NOT NULL, 
                    order_date DATETIME DEFAULT CURRENT_TIMESTAMP 
                )
            ''')

            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_menu_callback_data ON menu (callback_data)')
            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_items_callback_data ON items (callback_data)')
            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_user_id ON orders (user_id)')

            categories = [
                ('Хлебобулочные изделия🥨', 'bakery'),
                ('Закуски🧀', 'snacks'),
                ('Салаты🥗', 'salads'),
                ('Супы🍲', 'soups'),
                ('Гарнир🍚', 'side_dishes'),
                ('Горячие блюда🥩', 'hot_dishes'),
                ('Десерт🧁', 'desserts'),
                ('Холодные напитки🍹', 'cold_drinks'),
                ('Горячие напитки🍵', 'hot_drinks'),
                ('Алкогольные напитки🥂', 'alcoholic_drinks')
            ]

            cursor.executemany('INSERT OR IGNORE INTO menu (name, callback_data) VALUES (?, ?)', categories)

            items = [
                ('bakery', 'Хлебная корзинка', 'bread_cart', 15),
                ('snacks', 'Зелень', 'greens', 30),
                ('snacks', 'Сырная тарелка', 'cheese_plate', 200),
                ('snacks', 'Мясная тарелка', 'meat_plate', 250),
                ('salads', 'Греческий салат', 'greek_salad', 150),
                ('salads', 'Болгарский салат', 'bulgarian_salad', 140),
                ('salads', 'Моцарелла капрезе', 'mozzarella_caprese', 180),
                ('soups', 'Томатный крем-суп', 'tomato_soup', 150),
                ('soups', 'Суп с курицей', 'chicken_soup', 140),
                ('soups', 'Солянка', 'solyanka', 160),
                ('side_dishes', 'Картофель фри', 'french_fries', 70),
                ('side_dishes', 'Рис', 'rice', 60),
                ('hot_dishes', 'Шашлык ассорти', 'barbeque', 300),
                ('hot_dishes', 'Говяжий стейк', 'beef_steak', 400),
                ('hot_dishes', 'Курица в духовке', 'baked_chicken', 280),
                ('desserts', 'Брауни', 'brownie', 120),
                ('desserts', 'Чизкейк', 'cheesecake', 150),
                ('desserts', 'Мороженое', 'ice_cream', 90),
                ('cold_drinks', 'Вода', 'water', 50),
                ('cold_drinks', 'Минеральная вода', 'mineral_water', 60),
                ('cold_drinks', 'Кока-Кола', 'coke', 80),
                ('cold_drinks', 'Натуральный сок', 'juice', 100),
                ('hot_drinks', 'Чай', 'tea', 40),
                ('hot_drinks', 'Кофе', 'coffee', 90),
                ('hot_drinks', 'Горячий шоколад', 'hot_chocolate', 120),
                ('alcoholic_drinks', 'Водка', 'vodka', 210),
                ('alcoholic_drinks', 'Вино', 'wine', 300),
                ('alcoholic_drinks', 'Виски', 'whisky', 450)
            ]

            cursor.executemany(
                'INSERT OR IGNORE INTO items '
                '(category_callback, name, callback_data, price) VALUES (?, ?, ?, ?)', items
            )

            logger.info("База данных и таблицы успешно созданы или уже существуют.")
    except sqlite3.Error as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise


def db_connection(func):
    """Декоратор для подключения к базе данных."""
    def wrapper(*args, **kwargs):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                kwargs['conn'] = conn
                return func(*args, **kwargs)
        except sqlite3.Error as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
    return wrapper


@db_connection
def execute_query(query, params=(), conn=None):
    """Выполнение SQL-запроса."""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Ошибка выполнения запроса: {e}")
        raise


@db_connection
def fetch_all(query, params=(), conn=None):
    """Получение всех результатов SQL-запроса."""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Ошибка выполнения запроса: {e}")
        return []
