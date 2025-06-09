from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()
    confirm = State()
    complete = State()


class OrderStates(StatesGroup):
    start_order = State()
    size = State()
    additives = State()
    confirm = State()
