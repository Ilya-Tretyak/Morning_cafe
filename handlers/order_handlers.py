import json
from typing import Union

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN, ADMINS_ID
from database.database import (
    get_users_basket,
    create_order,
    get_users_orders,
    get_menu,
    get_sizes,
    get_additives,
)
from keyboards import inline_kb, reply_kb

router = Router()
bot = Bot(token=BOT_TOKEN)


@router.callback_query(F.data == "basket_checkout")
async def basket_checkout(callback: CallbackQuery, state: FSMContext):
    """Оформление заказа"""
    user_id = callback.from_user.id
    basket = get_users_basket(user_id)

    if basket:
        total_sum_item = 0
        menu_dict = {item[0]: item for item in get_menu()}
        sizes_dict = {item[0]: item for item in get_sizes()}
        additives_dict = {item[0]: item for item in get_additives()}
        for i, j, product_id, size_id, additive_id in basket:
            total_sum_item += float(menu_dict[product_id][3]) * sizes_dict[size_id][2] + float(additives_dict[additive_id][2])

        order_id = create_order(user_id, total_sum_item)
        await callback.message.delete()

        await callback.message.answer(
            f"✅ Ваш заказ #{order_id} оформлен!\n Спасибо ☕",
            reply_markup=inline_kb.orders_button
        )

        order_text = "".join(
            f"\n\n        <b>{menu_dict[product_id][1]}</b>\n"
            f"Объем: <b>{sizes_dict[size_id][1]}</b>\n"
            f"Дополнительно: <b>{additives_dict[additive_id][1]}</b>" for i, j, product_id, size_id, additive_id in basket
        )

        for admin_id in ADMINS_ID:
            await callback.message.answer(text="Админ-панель",reply_markup=reply_kb.admin_menu_keyboard)
            await bot.send_message(
                chat_id=admin_id,
                text=f"🔔🔔🔔Новый заказ🔔🔔🔔\n\n"
                     f"Заказ #<b><u>{order_id}</u></b>\n\n"
                     f"Состав заказа:{order_text}\n\n"
                     f"Общая сумма: <b>{total_sum_item}</b> руб.",
                parse_mode="HTML",
                reply_markup=inline_kb.requested_orders_item_keyboard(order_id)
            )

        await state.clear()
    else:
        await callback.message.answer("🧺 Корзина пуста. Добавьте товары перед заказом.")
    await callback.answer()


@router.message(F.text == "Заказы 📝")
@router.callback_query(F.data == "orders")
async def get_order_by_user(message_or_cb: Union[Message, CallbackQuery], ):
    """Список заказов для ПОЛЬЗОВАТЕЛЯ"""
    if isinstance(message_or_cb, CallbackQuery):
        message = message_or_cb.message
        user_id = message_or_cb.from_user.id
        await message_or_cb.answer()
    else:
        message = message_or_cb
        user_id = message_or_cb.from_user.id

    orders = get_users_orders(user_id)
    print("orders", orders)
    if orders:
        for order in orders:
            print("order", order)
            menu = get_menu()
            sizes = get_sizes()
            additives = get_additives()

            order_product = json.loads(order[2])
            text = f"📝Ваш заказ #{order[0]}:\n\n"

            for item in order_product:
                title = menu[item['product_id'] - 1][1]
                size = sizes[item['size_id'] - 1][1]
                additive = additives[item['additive_id'] - 1][1]
                text += (f"        <b><u>{title}</u></b>\n\n"
                         f"<u>Размер:</u> <b>{size}</b>\n"
                         f"<u>Добавки:</u> <b>{additive}</b>\n"
                         f"__________________________\n\n")

            text += (f"<u>Сумма заказа:</u> <b>{order[4]} руб.\n</b>"
                     f"<u>Статус заказа:</u> <b>{order[3]}</b>")
            await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("📝 У вас нет активных заказов.")

