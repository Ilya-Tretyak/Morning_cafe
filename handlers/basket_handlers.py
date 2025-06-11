from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.fsm.context import FSMContext

from typing import Union

from config.settings import BOT_TOKEN
from handlers.menu_handlers import menu_handler
from keyboards import inline_kb
from ustils.state import OrderStates
from database.database import (get_menu, get_sizes,
                               get_additives,
                               add_item_in_basket,
                               get_users_basket,
                               del_item_in_basket)


router = Router()
bot = Bot(token=BOT_TOKEN)

sizes = {s[0]: s for s in get_sizes()}
additives = {a[0]: a for a in get_additives()}
menu = {m[0]: m for m in get_menu()}


@router.message(F.text == "Корзина 🧺")
@router.callback_query(F.data == "basket")
async def show_users_basket(
        update: Union[Message, CallbackQuery],
        state: FSMContext
):
    """Получения пользователем совей корзины"""
    if isinstance(update, CallbackQuery):
        message = update.message
        user_id = update.from_user.id
        await update.answer()
    else:
        message = update
        user_id = update.from_user.id

    basket = get_users_basket(user_id)

    if not basket:
        await message.answer("🧺 Ваша корзина пуста.")
        return

    await state.update_data(
        basket=basket,
        current_index=0,
        menu={item[0]: item for item in get_menu()},
        sizes={s[0]: s for s in get_sizes()},
        additives={a[0]: a for a in get_additives()}
    )

    await show_basket_item(message, state)


async def show_basket_item(message_or_cb, state: FSMContext):
    """Отображение отдельной позиции из корзины с навигацией по ней"""
    data = await state.get_data()
    basket = data['basket']
    index = data['current_index']
    menu = data['menu']
    sizes = data['sizes']
    additives = data['additives']

    if index < 0 or index >= len(basket):
        await message_or_cb.answer("Ошибка отображения корзины.")
        return

    item = basket[index]
    basket_id, user_id, product_id, size_id, additive_id = item

    product = menu.get(product_id)
    size = sizes.get(size_id)
    additive = additives.get(additive_id)

    total_sum_item = 0
    for i, j, product_id, size_id, additive_id in basket:
        total_sum_item += float(menu[product_id][3]) * sizes[size_id][2] + float(additives[additive_id][2])

    text = (f"<u>{product[1]}</u>\n\n"
            f"<b>Цена:</b> {int(product[3] * size[2])} руб.\n"
            f"<b>Размер:</b> {size[1]}\n"
            f"<b>Добавка:</b> {additive[1]} (+ {additive[2]} руб).\n\n"
            f"{index + 1} из {len(basket)}\n\n"
            f"Цена за кофе: {int(product[3] * size[2] + additive[2])} руб.\n"
            f"----------------------\n"
            f"<b>Общая сумма корзины: {int(total_sum_item)} руб.</b>")

    try:
        await message_or_cb.answer_photo(
            photo=FSInputFile(product[4]),
            caption=text,
            reply_markup=inline_kb.basket_navigation_keyboard(basket_id),
            parse_mode="HTML"
        )
    except FileNotFoundError:
        await message_or_cb.answer(
            text=f"{text}\n\n⚠️ Фото не найдено",
            reply_markup=inline_kb.basket_navigation_keyboard(basket_id),
            parse_mode="HTML"
        )


@router.callback_query(F.data.in_(["basket_prev", "basket_next"]))
async def navigate_basket(callback: CallbackQuery, state: FSMContext):
    """Реализация навигации"""
    data = await state.get_data()
    index = data['current_index']
    basket = data['basket']

    if callback.data == "basket_prev":
        index = (index - 1) % len(basket)
    else:
        index = (index + 1) % len(basket)

    await state.update_data(current_index=index)
    await callback.message.delete()
    await show_basket_item(callback.message, state)
    await callback.answer()


@router.callback_query(F.data.startswith("basket_delete:"))
async def delete_item_in_basket(callback: CallbackQuery, state: FSMContext):
    """Удаления позиции из корзины пользователем"""
    basket_id = int(callback.data.split(":")[1])
    del_item_in_basket(basket_id)

    basket = get_users_basket(callback.from_user.id)
    if not basket:
        await callback.message.delete()
        await callback.message.answer("🧺 Ваша корзина пуста.")
        await state.clear()
        await callback.answer()
        return

    await state.update_data(basket=basket, current_index=0)
    await show_basket_item(callback.message, state)
    await callback.answer("Удалено ✅", show_alert=True)


@router.callback_query(F.data.startswith("add_to_order:"))
async def add_to_basket(callback: CallbackQuery, state: FSMContext):
    """Выбор размера кофе"""
    await state.update_data(
        product_id=int(callback.data.split(":")[1]),
        product_title=callback.message.caption.split(" ")[0]
    )
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile("database/images/sizes.jpg"),
            caption="Выберете размер кофе"
        ),
        reply_markup=inline_kb.sizes_inline_keyboard
    )
    await state.set_state(OrderStates.size)
    await callback.answer()





@router.callback_query(F.data.startswith("size:"))
async def process_sizes(callback: CallbackQuery, state: FSMContext):
    """Добавление допов(молоко, сахар)"""
    await state.update_data(size_id=int(callback.data.split(":")[1]), size_title=callback.message.caption)
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile("database/images/dopping.jpg"),
            caption="Добавить к кофе"
        ),
        reply_markup=inline_kb.additives_inline_keyboard
    )
    await state.set_state(OrderStates.additives)
    await callback.answer()


@router.callback_query(F.data.startswith("additives:"))
async def process_additives(callback: CallbackQuery, state: FSMContext):
    """Подтверждение выбранной позиции"""
    await state.update_data(additives_id=int(callback.data.split(":")[1]))
    data = await state.get_data()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile("database/images/coffee_cooking.jpg"),
            caption=f"Проверим ваш заказ:\n\n"
                    f"<u>{data['product_title']}</u>\n"
                    f"Размер: {sizes[data['size_id']][1]}\n"
                    f"Добавка: {additives[data['additives_id']][1]}\n",
            parse_mode="HTML"
        ),
        reply_markup=inline_kb.add_in_basket_keyboard
    )
    await state.set_state(OrderStates.confirm)
    await callback.answer()


@router.callback_query(F.data.startswith("add_in_basket"))
async def add_in_basket(callback: CallbackQuery, state: FSMContext):
    """Добавление в корзину"""
    data = await state.get_data()

    user_id = callback.from_user.id
    product_id = data['product_id']
    size_id = data['size_id']
    additives_id = data['additives_id']

    add_item_in_basket(user_id, product_id, size_id, additives_id)
    await callback.answer("Товар добавлен в корзину!", show_alert=True)
    await state.clear()
    await menu_handler(callback.message, state)

    await callback.answer()


@router.callback_query(F.data.startswith("dont_add_in_basket"))
async def add_in_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Заказ позиции отменен!", show_alert=True)
    await state.clear()
    await menu_handler(callback.message, state)

    await callback.answer()


