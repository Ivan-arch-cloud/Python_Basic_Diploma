from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from restaurant_bot.database.db import fetch_all


def get_categories_keyboard() -> InlineKeyboardMarkup:
    """Создаёт инлайн-клавиатуру для категорий."""
    keyboard = InlineKeyboardMarkup()
    query = "SELECT name, callback_data FROM menu"
    categories = fetch_all(query)

    for name, callback_data in categories:
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"category_{callback_data}"))

    return keyboard


def get_items_keyboard() -> InlineKeyboardMarkup:
    """Создаёт инлайн-клавиатуру для блюд в выбранной категории."""
    keyboard = InlineKeyboardMarkup()
    query = "SELECT name, callback_data, price FROM items WHERE category_callback = ?"
    items = fetch_all(query)

    for name, callback_data, price in items:
        button_text = f"{name} - {price}₽"
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=f"item_{callback_data}"))

    # Кнопка "Назад" для возврата к категориям
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_categories"))

    return keyboard


def get_back_button_inline() -> InlineKeyboardMarkup:
    """Создает inline кнопку 'Назад'."""
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_to_categories")
    keyboard.add(back_button)
    return keyboard

