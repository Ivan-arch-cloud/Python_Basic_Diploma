from telebot.types import CallbackQuery
from restaurant_bot.keyboards.inline.inline import get_categories_keyboard, get_items_keyboard, get_back_button_inline
import logging
from telebot import TeleBot

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_menu_handlers(bot: TeleBot):
    @bot.message_handler(commands=['menu'])
    def send_categories(message):
        """Отправляет категории."""
        logger.info(f"User {message.chat.id} requested menu.")
        keyboard = get_categories_keyboard()
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите категорию:",
            reply_markup=keyboard
        )


    @bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
    def handle_category_selection(call: CallbackQuery):
        """Обрабатывает выбор категории и показывает блюда с кнопкой 'Назад'."""
        category_callback = call.data.split("category_")[1]
        logger.info(f"User {call.message.chat.id} selected category: {category_callback}")

        keyboard = get_items_keyboard(category_callback)

        # Добавляем кнопку "Назад" к inline клавиатуре
        back_button = get_back_button_inline()
        keyboard.add(back_button.inline_keyboard[0][0])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите блюдо:",
            reply_markup=keyboard
        )


    @bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
    def handle_item_selection(call: CallbackQuery):
        """Обрабатывает выбор блюда."""
        item_callback = call.data.split("item_")[1]
        logger.info(f"User {call.message.chat.id} selected item: {item_callback}")

        # Обработка выбора блюда: можно добавить в корзину или просто уведомить пользователя
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=f"Вы выбрали блюдо: {item_callback}"
        )

        # Предлагаем вернуться к категориям или продолжить выбор
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Вы можете вернуться назад, чтобы выбрать другую категорию.",
            reply_markup=get_back_button_inline()  # Используем inline-кнопку
        )
