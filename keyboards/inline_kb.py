from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_navigation_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Inline-навигация для позиций в меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_item"),
            InlineKeyboardButton(text="Далее ➡️", callback_data="next_item")
        ],
        [InlineKeyboardButton(text="Добавить➕", callback_data=f"add_to_order:{product_id}")],
        [InlineKeyboardButton(text="Корзина 🧺", callback_data=f"basket")],
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
        [InlineKeyboardButton(text="Молоко 🥛", callback_data="additives:2")],
        [InlineKeyboardButton(text="Корица 🧂", callback_data="additives:3")],
        [InlineKeyboardButton(text="Сахар 🧂", callback_data="additives:4")],
        [InlineKeyboardButton(text="Лимон 🍋", callback_data="additives:5")],
        [InlineKeyboardButton(text="Ничего ❌", callback_data="additives:1")]
    ]
)

"""Inline-keyboard добавления или отмены заказа"""
add_in_basket_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить в корзину ✅", callback_data="add_in_basket")],
        [InlineKeyboardButton(text="❎ Отменить заказ", callback_data="dont_add_in_basket")]
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

orders_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Заказы 📝", callback_data="orders")],
    ]
)

def requested_orders_item_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти к заказу ➡️", callback_data=f"requested_orders:{order_id}")],
        ]
    )

def delete_item_navigation_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Inline-навигация для позиций в меню-удаление"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_item"),
            InlineKeyboardButton(text="Далее ➡️", callback_data="next_item")
        ],
        [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_item")],
    ])

def get_admin_all_orders_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Inline-навигация по заказам для админа"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Посмотреть заказ 📥", callback_data=f"switch_status:{order_id}")],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_order"),
                InlineKeyboardButton(text="Далее ➡️", callback_data="next_order")
            ],
            [InlineKeyboardButton(text="Изменить статус заказа 🕚", callback_data=f"switch_status:{order_id}")],
    ])

def status_order_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Готовиться", callback_data="update_status:cook")],
            [InlineKeyboardButton(text="Заказ готов", callback_data="update_status:done")]
        ]
    )
