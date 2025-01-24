from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_category_keyboard():
    keyboard = InlineKeyboardMarkup()
    categories = [
        "холодные напитки", "горячие напитки", "алкогольные напитки",
        "салаты", "гарнир", "закуски", "хлебобулочные изделия",
        "горячее блюдо", "десерт"
    ]
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category, callback_data=f"category_{category}"))
    return keyboard
