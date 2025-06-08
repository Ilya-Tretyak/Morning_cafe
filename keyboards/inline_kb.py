from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu_navigation = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_item"),
            InlineKeyboardButton(text="Далее ➡️", callback_data="next_item")
        ],
        [InlineKeyboardButton(text="Добавить в корзину✅", callback_data="in_basket")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close_menu")]
    ])
