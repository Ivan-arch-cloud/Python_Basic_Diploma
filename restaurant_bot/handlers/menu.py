import telebot
import os
from telebot import types
from dotenv import load_dotenv
from restaurant_bot.keyboards.inline import create_inline_keyboard
from restaurant_bot.keyboards.reply import create_reply_keyboard

# Создаём объект бота
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Получаем токен из переменной окружения
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Привет! Я готов помочь с заказом. Используйте команду /menu для выбора категории."
    )

# Обработчик для команды /menu с reply клавиатурой
@bot.message_handler(commands=['menu'])
def show_menu(message: types.Message):
    # Используем reply клавиатуру
    reply_keyboard = create_reply_keyboard()
    bot.send_message(
        message.chat.id,
        "Выберите опцию из меню:",
        reply_markup=reply_keyboard
    )

# Обработчик для команды /cancel
@bot.message_handler(commands=['cancel'])
def cancel_order(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Ваш заказ был отменён."
    )

# Обработчик для inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call: types.CallbackQuery):
    if call.data == "cold_drinks":
        bot.send_message(call.message.chat.id, "Вы выбрали холодные напитки.")
    elif call.data == "hot_drinks":
        bot.send_message(call.message.chat.id, "Вы выбрали горячие напитки.")
    elif call.data == "alcoholic_drinks":
        bot.send_message(call.message.chat.id, "Вы выбрали алкогольные напитки.")
    elif call.data == "salads":
        bot.send_message(call.message.chat.id, "Вы выбрали салаты.")
    elif call.data == "garnishes":
        bot.send_message(call.message.chat.id, "Вы выбрали гарнир.")

# Регистрируем обработчики
def register_custom_handlers():
    # Здесь уже используется декоратор, поэтому нет необходимости в дополнительных регистрациях
    pass  # Не нужно ничего делать, обработчики уже зарегистрированы через декораторы

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
