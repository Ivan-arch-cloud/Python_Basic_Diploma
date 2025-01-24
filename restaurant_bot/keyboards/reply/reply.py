from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from restaurant_bot.loader import bot


def role_selection_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура для выбора роли: Админ или Пользователь.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    admin_button = KeyboardButton("Админ")
    users_button = KeyboardButton("Пользователь")
    keyboard.add(admin_button, users_button)

    return keyboard


def after_role_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура для действий после выбора роли.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    enter_password_button = KeyboardButton("Ввести пароль")
    keyboard.add(enter_password_button)

    return keyboard

def get_back_button() -> ReplyKeyboardMarkup:
    """Функция для создания кнопки 'Назад'."""
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Назад"))


def get_cart_keyboard():
    """Клавиатура для корзины."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Посмотреть корзину")
    button2 = KeyboardButton("Оформить заказ")
    button3 = KeyboardButton("Отменить заказ")
    keyboard.add(button1, button2, button3)
    return keyboard

