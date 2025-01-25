from telebot.types import Message
from telebot import TeleBot
from restaurant_bot.keyboards.reply.reply import role_selection_keyboard
from restaurant_bot.states.user_information import UserInfoStates, AdminStates, UsersStates


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start_handler(message: Message) -> None:
        """
        Команда /start: спрашиваем, кто пользователь.
        """
        bot.set_state(message.from_user.id, UserInfoStates.user_role, message.chat.id)
        bot.send_message(
            message.from_user.id,
            "Добро пожаловать в наш ресторан😍! Кто вы? Выберите подходящую кнопку.",
            reply_markup=role_selection_keyboard()
        )

    @bot.message_handler(state=UserInfoStates.user_role)
    def get_user_role(message: Message) -> None:
        """
        Обработка роли пользователя: администратор или обычный пользователь.
        """
        if message.text.lower() == 'админ':
            bot.send_message(
                message.from_user.id,
                "Вы выбрали роль Админа. Введите пароль, пожалуйста.",
            )
            bot.set_state(message.from_user.id, AdminStates.admin_password_check, message.chat.id)

        elif message.text.lower() == 'пользователь':
            bot.send_message(
                message.from_user.id,
                "Вы выбрали роль пользователя. Заказывайте наши вкусняшки.🍴💖"
            )
            bot.set_state(message.from_user.id, UsersStates.user_name, message.chat.id)

        else:
            bot.send_message(
                message.from_user.id,
                "Пожалуйста, выберите роль, нажав на кнопку: 'Админ' или 'Пользователь'."
            )