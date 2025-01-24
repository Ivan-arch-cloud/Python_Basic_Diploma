from ..loader import bot
from ..states.user_information import AdminState
from ..keyboards.reply.reply import role_selection_keyboard, after_role_keyboard
from ..database.admin_db import get_admin_password, check_admin_password, update_admin_password
from telebot.types import Message


@bot.message_handler(func=lambda msg: msg.text == "Админ")
def admin_selected(message: Message):
    """
    Обработчик выбора роли "Админ".
    """
    existing_password = get_admin_password()
    if not existing_password:
        bot.send_message(message.chat.id, "Пароль администратора не установлен. Пожалуйста, установите пароль.")
        bot.set_state(message.from_user.id, AdminState.admin_name, message.chat.id)
        bot.send_message(message.chat.id, "Введите новый пароль для администратора.")
    else:
        bot.send_message(message.chat.id, "Для доступа к панели администратора введите пароль.")
        bot.set_state(message.from_user.id, AdminState.admin_password, message.chat.id)


@bot.message_handler(func=lambda msg: msg.text == "Ввести пароль")
def enter_password(message: Message) -> None:
    """
    Обработчик кнопки "Ввести пароль".
    """
    bot.set_state(message.from_user.id, AdminState.admin_password, message.chat.id)
    bot.send_message(message.chat.id, "Введите пароль", reply_markup=None)


@bot.message_handler(func=lambda msg: msg.text == "Вернуться назад")
def bac_to_role_selection(message: Message) -> None:
    """
    Обработчик кнопки "Вернуться назад".
    """
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "Кто вы? Выберите подходящую кнопку.", reply_markup=role_selection_keyboard())


@bot.message_handler(state=AdminState.admin_password)
def verify_admin_password(message: Message) -> None:
    """
    Обработчик ввода пароля администратора.
    """
    input_password = message.text
    if check_admin_password(input_password):
        bot.send_message(message.chat.id, "Пароль принят. Вы вошли в панель администратора.")
        bot.set_state(message.from_user.id, AdminState.admin_name, message.chat.id)
        bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=after_role_keyboard())
    else:
        bot.send_message(message.chat.id, "Неверный пароль. Попробуйте снова.")


@bot.message_handler(func=lambda msg: msg.text == "Изменить пароль")
def change_password(message: Message) -> None:
    """
    Предложить админу изменить пароль.
    """
    bot.send_message(message.chat.id, "Введите новый пароль для администратора.")
    bot.set_state(message.from_user.id, AdminState.admin_password, message.chat.id)


@bot.message_handler(state=AdminState.admin_password)
def update_admin_password_handler(message: Message) -> None:
    """
    Обработчик ввода нового пароля.
    """
    new_password = message.text
    update_admin_password(new_password)  # Эта функция обновляет пароль в базе данных
    bot.send_message(message.chat.id, "Пароль администратора успешно обновлён.")
    bot.set_state(message.from_user.id, AdminState.admin_name, message.chat.id)
