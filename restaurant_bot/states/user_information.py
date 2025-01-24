from telebot.handler_backends import State, StatesGroup


class AdminState(StatesGroup):
    admin_name = State()
    admin_id = State()
    admin_open_menu = State()
    admin_update_menu = State()
    today_is_order = State()
    confirm_save_changes = State()


class UsersState(StatesGroup):
    user_name = State()
    menu = State()
    shopping_cart = State()
    total_amount = State()
    payment = State()
    address = State()
    phone_number = State()