from telebot.handler_backends import State, StatesGroup


class UserInfoStates(StatesGroup):
    user_role = State()


class AdminStates(StatesGroup):
    admin_password_check = State()
    add_item_name = State()
    add_item_price = State()
    change_price_item = State()
    change_price_value = State()
    delete_item_name = State()
    view_today_is_order = State()


class UsersStates(StatesGroup):
    user_name = State()
    check_name = State()
    shopping_cart = State()
    add_to_cart = State()
    remove_from_cart = State()
    total_amount = State()
    payment = State()
    address = State()
    phone_number = State()

