from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Меню ☕️")],
        [KeyboardButton(text="Корзина 🗑️")],
    ],
    resize_keyboard=True
)
start_register_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зарегистрироваться✍️")],
    ],
    resize_keyboard=True
)

yes_or_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да✅"), KeyboardButton(text="Нет❌")],
    ],
    resize_keyboard=True
)
