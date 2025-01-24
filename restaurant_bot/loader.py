from telebot import TeleBot
from config_data.config import BOT_TOKEN



bot = TeleBot(BOT_TOKEN, parse_mode="HTML")
