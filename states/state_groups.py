from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class RegistrationSG(StatesGroup):
    greeting = State()
    rules = State()
    manual = State()


class startSG(StatesGroup):
    start = State()
    workers = State()

    profile = State()

    market = State()
    services_market = State()

    manual = State()
    watch_manual = State()

    admins = State()

    about = State()
    rules = State()


class adminSG(StatesGroup):
    start = State()

    choose_malling = State()
    get_mail = State()
    get_time = State()
    get_keyboard = State()
    confirm_mail = State()

    deeplink_menu = State()
    deeplink_del = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()
