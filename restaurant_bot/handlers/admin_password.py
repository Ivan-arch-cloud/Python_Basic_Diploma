import logging
import hashlib
from restaurant_bot.keyboards.reply.reply import after_role_keyboard, get_back_button
from restaurant_bot.database.db import fetch_all
from restaurant_bot.states.user_information import AdminStates
from telebot import TeleBot
from telebot.types import Message


logger = logging.getLogger(__name__)


def admin_password_handler(bot: TeleBot):

    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # Проверка корректности пароля
    def is_password_correct(entered_password: str) -> bool:
        hashed_password = hash_password(entered_password)
        query = "SELECT password FROM admin WHERE id = 1"
        result = fetch_all(query)
        if result:
            stored_password = result[0][0]
            return hashed_password == stored_password
        return False


    @bot.message_handler(state=AdminStates.admin_password_check)
    def verify_password_handler(message: Message) -> None:
        entered_password = message.text.strip()

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            # Инициализируем количество попыток
            if 'failed_attempts' not in data:
                data['failed_attempts'] = 0

            if is_password_correct(entered_password):
                bot.send_message(message.chat.id,
                                 "Пароль верный. Добро пожаловать, Админ! 😊",
                                 reply_markup=after_role_keyboard())  # Клавиатура для дальнейших действий
                logger.info(f"Пароль админа подтвержден для пользователя {message.from_user.id}.")
                bot.delete_state(message.from_user.id, message.chat.id)
                data.clear()  # Очищаем данные после успешного входа
            else:
                data['failed_attempts'] += 1
                bot.send_message(
                    message.chat.id,
                    f"Пароль неверный. Попробуйте снова. Попыток: {data['failed_attempts']}.",
                    reply_markup=get_back_button()  # Кнопка для возврата назад
                )
                logger.warning(
                    f"Неверный пароль для администратора от пользователя {message.from_user.id}. "
                    f"Количество попыток: {data['failed_attempts']}."
                )

                # Если превышено количество попыток
                if data['failed_attempts'] >= 3:
                    bot.send_message(
                        message.chat.id,
                        "Вы превысили допустимое количество попыток. Попробуйте позже."
                    )
                    bot.delete_state(message.from_user.id, message.chat.id)
                    data.clear()