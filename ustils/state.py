from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()
    confirm = State()
    complete = State()


class BasketStates(StatesGroup):
    view_order = State()
    address = State()
    time = State()
    confirm = State()
    payment = State()
