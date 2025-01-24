import hashlib
import logging
from restaurant_bot.database.db import execute_query, fetch_all
from restaurant_bot.config_data.config import ADMIN_PASSWORD

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Хеширование пароля."""
    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as e:
        logger.error(f"Ошибка при хешировании пароля: {e}")
        raise


def init_admin_table():
    """Инициализация таблицы администратора."""
    try:
        query = '''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL
            )
        '''
        execute_query(query)
        logger.info("Таблица администратора успешно создана или уже существует.")

        query_check = "SELECT 1 FROM admin LIMIT 1"
        if not fetch_all(query_check):
            # Получаем пароль администратора из .env
            default_password = ADMIN_PASSWORD
            if not default_password:
                raise ValueError("Пароль администратора не установлен в .env")

            hashed_password = hash_password(default_password)
            execute_query("INSERT INTO admin (password) VALUES (?)", (hashed_password,))
            logger.info("Пароль администратора установлен.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации таблицы admin: {e}")
        raise
