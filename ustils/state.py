from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """Состояния для регистрации"""
    full_name = State()
    phone_number = State()
    confirm = State()
    complete = State()


class OrderStates(StatesGroup):
    """Состояния для добавления в корзину"""
    start_order = State()
    size = State()
    additives = State()
    confirm = State()
