from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


"""Reply-keyboard главного меню"""
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Меню ☕️")],
        [KeyboardButton(text="Корзина 🗑️")],
    ],
    resize_keyboard=True
)

"""Reply-keyboard начало регистрации"""
start_register_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зарегистрироваться✍️")],
    ],
    resize_keyboard=True
)

"""Reply-keyboard да\нет"""
yes_or_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да✅"), KeyboardButton(text="Нет❌")],
    ],
    resize_keyboard=True
)
