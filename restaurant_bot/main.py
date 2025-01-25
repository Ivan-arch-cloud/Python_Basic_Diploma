from restaurant_bot.handlers.start import register_handlers
from restaurant_bot.handlers.admin_password import admin_password_handler
from restaurant_bot.handlers.admin import register_admin_handlers
from restaurant_bot.handlers.users import register_user_handler
from restaurant_bot.handlers.menu import register_menu_handlers
from restaurant_bot.handlers.help import register_help_handlers
import telebot
from restaurant_bot.config_data.config import BOT_TOKEN
from telebot.storage import StateMemoryStorage
from restaurant_bot.database.db import init_db

bot = telebot.TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage(), parse_mode="HTML")

register_handlers(bot)
register_admin_handlers(bot)
admin_password_handler(bot)
register_user_handler(bot)
register_menu_handlers(bot)
register_help_handlers(bot)

if __name__ == '__main__':
    init_db()  # Создание таблиц, если их нет
    bot.polling(none_stop=True)