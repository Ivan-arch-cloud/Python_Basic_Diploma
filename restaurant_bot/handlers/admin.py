from restaurant_bot.database.rest_db_for_admin import (
    add_item_to_menu,
    update_item_price,
    delete_item,
    get_orders_for_today,
    format_orders,
)
from restaurant_bot.states.user_information import AdminStates
from restaurant_bot.keyboards.reply.reply import get_back_button
from telebot.types import Message
from telebot import TeleBot


def register_admin_handlers(bot: TeleBot):
    @bot.message_handler(commands=["add"])
    def start_add_item_process(message: Message):
        """Начало процесса добавления блюда."""
        bot.set_state(message.from_user.id, AdminStates.add_item_name, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Вы начали процесс добавления нового блюда. "
            "Введите название блюда или нажмите 'Назад' для отмены.",
            reply_markup=get_back_button()
        )


    @bot.message_handler(state=AdminStates.add_item_name)
    def get_item_name(message: Message):
        """Получение названия блюда."""
        if not message.text.strip():
            bot.send_message(message.chat.id, "Ошибка: название блюда не может быть пустым.")
            return

        if message.text.strip().lower() == "/exit":
            exit_process(message)
            return

        item_name = message.text.strip()
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['item_name'] = item_name

        bot.set_state(message.from_user.id, AdminStates.add_item_price, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Название сохранено! Теперь введите цену блюда (только положительное число).",
            reply_markup=get_back_button()
        )


    @bot.message_handler(state=AdminStates.add_item_price)
    def get_item_price(message: Message):
        """Получение цены блюда."""
        if not message.text.strip():
            bot.send_message(message.chat.id, "Ошибка: цена блюда не может быть пустой.")
            return

        if message.text.strip().lower() == "/exit":
            exit_process(message)
            return

        try:
            item_price = float(message.text.strip())
            if item_price <= 0:
                raise ValueError("Цена должна быть положительным числом.")

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                item_name = data['item_name']
                add_item_to_menu(item_name, item_price)

            bot.send_message(
                message.chat.id,
                f"Блюдо '{item_name}' с ценой {item_price} успешно добавлено в меню! 🍽"
            )
            bot.delete_state(message.from_user.id, message.chat.id)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "Ошибка: введите корректную положительную цену.",
                reply_markup=get_back_button()
            )


    @bot.message_handler(commands=["change_price"])
    def start_change_price_process(message: Message):
        """Начало процесса изменения цены блюда."""
        bot.set_state(message.from_user.id, AdminStates.change_price_item, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Введите название блюда, для которого нужно изменить цену:",
            reply_markup=get_back_button()
        )


    @bot.message_handler(state=AdminStates.change_price_item)
    def change_price_handler(message: Message):
        """Обработчик изменения цены блюда."""
        if not message.text.strip():
            bot.send_message(message.chat.id, "Ошибка: название блюда не может быть пустым.")
            return

        if message.text.strip().lower() == "/exit":
            exit_process(message)
            return

        item_name = message.text.strip()
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['item_name'] = item_name

        bot.set_state(message.from_user.id, AdminStates.change_price_value, message.chat.id)
        bot.send_message(
            message.chat.id,
            f"Введите новую цену для блюда '{item_name}':",
            reply_markup=get_back_button()
        )


    @bot.message_handler(state=AdminStates.change_price_value)
    def set_new_price_handler(message: Message):
        """Установка новой цены блюда."""
        if not message.text.strip():
            bot.send_message(message.chat.id, "Ошибка: цена блюда не может быть пустой.")
            return

        if message.text.strip().lower() == "/exit":
            exit_process(message)
            return

        try:
            new_price = float(message.text.strip())
            if new_price <= 0:
                raise ValueError("Цена должна быть положительным числом.")

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                item_name = data['item_name']
                update_item_price(item_name, new_price)

            bot.send_message(
                message.chat.id,
                f"Цена блюда '{item_name}' успешно обновлена на {new_price}! 💰"
            )
            bot.delete_state(message.from_user.id, message.chat.id)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "Ошибка: введите корректную положительную цену.",
                reply_markup=get_back_button()
            )


    @bot.message_handler(commands=["delete_item"])
    def start_delete_item_process(message: Message):
        """Начало процесса удаления блюда."""
        bot.set_state(message.from_user.id, AdminStates.delete_item_name, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Введите название блюда, которое нужно удалить:",
            reply_markup=get_back_button()
        )


    @bot.message_handler(state=AdminStates.delete_item_name)
    def delete_item_handler(message: Message):
        """Обработчик удаления блюда."""
        if not message.text.strip():
            bot.send_message(message.chat.id, "Ошибка: название блюда не может быть пустым.")
            return

        if message.text.strip().lower() == "/exit":
            exit_process(message)
            return

        item_name = message.text.strip()
        if delete_item(item_name):
            bot.send_message(
                message.chat.id,
                f"Блюдо '{item_name}' успешно удалено из меню! 🗑"
            )
        else:
            bot.send_message(
                message.chat.id,
                f"Ошибка: блюдо '{item_name}' не найдено в меню.",
                reply_markup=get_back_button()
            )
        bot.delete_state(message.from_user.id, message.chat.id)


    @bot.message_handler(commands=["view_orders"])
    def start_view_orders_process(message: Message):
        """Начало процесса просмотра заказов за сегодня."""
        try:
            orders = get_orders_for_today()
            if orders:
                formatted_orders = format_orders(orders)
                bot.send_message(
                    message.chat.id,
                    f"Вот список заказов за сегодня:\n\n{formatted_orders}"
                )
            else:
                bot.send_message(message.chat.id, "На сегодня заказов пока нет. 😊")
        except Exception as e:
            bot.send_message(
                message.chat.id,
                "Произошла ошибка при получении заказов. Попробуйте позже."
            )
            print(f"Ошибка при получении заказов: {e}")


    @bot.message_handler(commands=["exit"], state="*")
    def exit_process(message: Message):
        """Выход из состояния и сброс данных."""
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Вы вышли из процесса. Если хотите начать заново, используйте нужную команду."
        )
