from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_navigation_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Inline-навигация для позиций в меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_item"),
            InlineKeyboardButton(text="Далее ➡️", callback_data="next_item")
        ],
        [InlineKeyboardButton(text="Добавить➕", callback_data=f"add_to_order:{product_id}")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close_menu")]
    ])

"""Inline-keyboard размера напитка"""
sizes_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="S (250 мл.) ☕️", callback_data="size:1")],
        [InlineKeyboardButton(text="M (280 мл.) ☕️", callback_data="size:2")],
        [InlineKeyboardButton(text="L (330 мл.) ☕️", callback_data="size:3")]
    ]
)

"""Inline-keyboard выбора допов"""
additives_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сахар 🧂", callback_data="additives:1")],
        [InlineKeyboardButton(text="Молоко 🥛", callback_data="additives:2")],
        [InlineKeyboardButton(text="Корица 🧂", callback_data="additives:3")],
        [InlineKeyboardButton(text="Лимон 🍋", callback_data="additives:4")],
    ]
)

"""Inline-keyboard добавления или отмены заказа"""
add_in_basket_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить в корзину ✅", callback_data="add_in_basket")],
        [InlineKeyboardButton(text="❎ Отменить заказ", callback_data="dont_add_in_basket")],
    ]
)

def basket_navigation_keyboard(basket_id):
    """Inline-keyboard навигация для корзины"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="basket_prev"),
            InlineKeyboardButton(text="➡️", callback_data="basket_next")
        ],
        [
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"basket_delete:{basket_id}")
        ],
        [
            InlineKeyboardButton(text="✅ Оформить заказ", callback_data="basket_checkout")
        ]
    ])
