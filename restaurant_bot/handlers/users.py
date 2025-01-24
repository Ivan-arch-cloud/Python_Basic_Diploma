import logging
from telebot.types import Message, CallbackQuery
from restaurant_bot.loader import bot
from restaurant_bot.states.user_information import UsersStates
from restaurant_bot.database.rest_db_for_users import (
    add_to_cart,
    view_cart,
    clear_cart,
    get_menu_items,
)
from restaurant_bot.keyboards.reply.reply import get_cart_keyboard
from restaurant_bot.keyboards.inline.inline import get_items_keyboard, get_back_button_inline

logger = logging.getLogger(__name__)

# user_name = State()
# check_name = State()
# shopping_cart = State()
# add_to_cart = State()
# remove_from_cart = State()
# total_amount = State()
# payment = State()
# address = State()
# phone_number = State()


@bot.message_handler(state=UsersStates.user_name)
def name_handler(message: Message) -> None:
    """Обработка ввода имени пользователя."""
    bot.send_message(message.chat.id, "Напишите ваше имя, пожалуйста.")
    bot.set_state(message.from_user.id, UsersStates.check_name, message.chat.id)


@bot.message_handler(state=UsersStates.check_name)
def check_name(message: Message) -> None:
    """Проверка введенного имени."""
    if message.text.isalpha():
        bot.send_message(
            message.chat.id,
            f"Спасибо, {message.text}! 😊 Теперь вы можете выбрать заказ.",
        )
        bot.set_state(message.from_user.id, UsersStates.shopping_cart, message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            "Имя должно содержать только буквы. Пожалуйста, введите корректное имя.",
        )


# Отображение меню
@bot.message_handler(state=UsersStates.shopping_cart, commands=["menu"])
def show_menu(message: Message) -> None:
    """Отправка категорий меню."""
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите категорию:",
        reply_markup=get_items_keyboard()
    )


@bot.callback_query_handler(state=UsersStates.add_to_cart, func=lambda call: call.data.startswith("item_"))
def handle_item_selection(call: CallbackQuery) -> None:
    """Обработка выбора блюда."""
    item_id = int(call.data.split("item_")[1])  # Получаем ID блюда
    try:
        add_to_cart(call.from_user.id, item_id)
        bot.answer_callback_query(call.id, "Блюдо добавлено в корзину! 🛒")
    except Exception as e:
        logger.error(f"Ошибка при добавлении в корзину: {e}")
        bot.answer_callback_query(call.id, "Ошибка при добавлении блюда. Попробуйте снова.")


# Просмотр корзины
@bot.message_handler(state=UsersStates.shopping_cart, commands=["cart"])
def view_user_cart(message: Message) -> None:
    """Просмотр содержимого корзины."""
    try:
        cart_items = view_cart(message.from_user.id)
        if cart_items:
            cart_text = "\n".join(
                [f"{item['name']} (x{item['quantity']}): {item['total_price']}₽" for item in cart_items]
            )
            bot.send_message(
                message.chat.id,
                f"Ваши товары в корзине:\n{cart_text}",
                reply_markup=get_cart_keyboard(),
            )
        else:
            bot.send_message(message.chat.id, "Ваша корзина пуста. Начните выбирать блюда!")
    except Exception as e:
        logger.error(f"Ошибка при просмотре корзины: {e}")
        bot.send_message(message.chat.id, "Ошибка при получении корзины. Попробуйте снова.")


# Очистка корзины
@bot.message_handler(state=UsersStates.remove_from_cart, commands=["clear_cart"])
def clear_user_cart(message: Message) -> None:
    """Очистка корзины пользователя."""
    try:
        if clear_cart(message.from_user.id):
            bot.send_message(message.chat.id, "Корзина успешно очищена! 🗑️")
        else:
            bot.send_message(message.chat.id, "Ошибка при очистке корзины. Попробуйте снова.")
    except Exception as e:
        logger.error(f"Ошибка при очистке корзины: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова.")


# Оформление заказа
@bot.message_handler(state=UsersStates.total_amount, commands=["checkout"])
def checkout_handler(message: Message) -> None:
    """Начало оформления заказа."""
    bot.send_message(message.chat.id, "Введите ваш адрес доставки:")
    bot.set_state(message.from_user.id, UsersStates.address, message.chat.id)


@bot.message_handler(state=UsersStates.address)
def address_handler(message: Message) -> None:
    """Сохранение адреса и запрос телефона."""
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    bot.set_state(message.from_user.id, UsersStates.phone_number, message.chat.id)


@bot.message_handler(state=UsersStates.phone_number)
def phone_number_handler(message: Message) -> None:
    """Сохранение номера телефона и подтверждение заказа."""
    bot.send_message(
        message.chat.id,
        "Спасибо! Ваш заказ оформлен и отправлен на обработку. 🛵",
    )
    bot.set_state(message.from_user.id, UsersStates.user_name, message.chat.id)
