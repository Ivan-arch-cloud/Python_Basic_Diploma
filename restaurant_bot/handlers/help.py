import logging
from telebot import TeleBot
from telebot.types import Message

logger = logging.getLogger(__name__)


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['help'])
    def help_handler(message: Message) -> None:
        """
        Команда /help: для пользователя.
        """
        logger.info(f"Команда /help получена от пользователя {message.from_user.id}.")
        bot.send_message(message.chat.id,
                         "Для административного входа, после команды '/start' "
                         "нажмите на 'Админ', после введите пароль. "
                         "Для пользовательского входа, после команды '/start' "
                         "нажмите на 'Пользователь', после введите ваше имя, чтобы сделать заказы. "
                         "Чтобы вернуться назад, нажмите на кнопку 'Вернуться назад'.",
                         )
