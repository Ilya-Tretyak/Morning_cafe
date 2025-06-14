from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


"""Reply-keyboard главного меню"""
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Меню ☕️")],
        [KeyboardButton(text="Корзина 🧺")],
        [KeyboardButton(text="Заказы 📝")],
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

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙Отменить")],
    ],
    resize_keyboard=True
)

admin_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Товары 🛒")],
        [KeyboardButton(text="Заказы 📥")],
        [KeyboardButton(text="🔙 В главное меню")],
    ],
    resize_keyboard=True
)


admin_menu_products_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить позицию в меню ➕")],
        [KeyboardButton(text="Удалить позицию из меню ❌")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)
