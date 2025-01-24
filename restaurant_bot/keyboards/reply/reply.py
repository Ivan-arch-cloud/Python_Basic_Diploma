from telebot.types import ReplyKeyboardMarkup

def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Категории", "Корзина")
    keyboard.add("Помощь")
    return keyboard
