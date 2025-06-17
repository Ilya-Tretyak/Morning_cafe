import os

from aiogram import Router, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN, ADMINS_ID
from handlers.command import admin_handler
from handlers.menu_handlers import show_menu
from keyboards import reply_kb, inline_kb
from keyboards.inline_kb import status_order_keyboard
from ustils.state import AdminCreateItemStates
from database.database import (
    add_item,
    get_menu,
    get_all_orders,
    get_user,
    switch_status_order
)

router = Router()
bot = Bot(token=BOT_TOKEN)


@router.message(F.text=="Товары 🛒")
async def admin_products_handler(message: Message):
    """Переход в админ-меню продукта"""
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    if message.from_user.id not in ADMINS_ID:
        return

    await message.answer("Меню товары 🛒:", reply_markup=reply_kb.admin_menu_products_keyboard)


@router.message(F.text=="🔙 Назад")
async def back_to_main_admin_menu(message: Message):
    """Возвращение в главное админ-меню"""
    return await admin_handler(message)


@router.message(F.text=="Добавить позицию в меню ➕")
async def start_create_products_handler(message: Message, state: FSMContext):
    """Добавления нового товара"""
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except TelegramBadRequest:
        pass

    if message.from_user.id not in ADMINS_ID:
        return

    await message.answer("Введите наименование новой позиции:", reply_markup=reply_kb.cancel_keyboard)
    await state.set_state(AdminCreateItemStates.start_create_item)


@router.message(AdminCreateItemStates.start_create_item)
async def create_process_title(message: Message, state: FSMContext):
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except TelegramBadRequest:
        pass

    if message.text != "🔙Отменить":
        await state.update_data(title=message.text)
        await message.answer(f"Введите описание для <b>{message.text}</b>:", reply_markup=reply_kb.cancel_keyboard, parse_mode="HTML")
        await state.set_state(AdminCreateItemStates.create_title_item)
    else:
        await message.answer("Создание новой позиции отменено!", show_alert=True)
        await state.clear()
        await admin_products_handler(message)


@router.message(AdminCreateItemStates.create_title_item)
async def create_process_description(message: Message, state: FSMContext):
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except TelegramBadRequest:
        pass

    if message.text != "🔙Отменить":
        await state.update_data(description=message.text)
        data = await state.get_data()
        await message.answer(
            f"Введите цену для <b>{data['title']}</b>:",
            reply_markup=reply_kb.cancel_keyboard,
            parse_mode="HTML"
        )
        await state.set_state(AdminCreateItemStates.create_description)
    else:
        await message.answer("Создание новой позиции отменено!", show_alert=True)
        await state.clear()
        await admin_products_handler(message)


@router.message(AdminCreateItemStates.create_description)
async def create_process_price(message: Message, state: FSMContext):
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except TelegramBadRequest:
        pass

    if message.text != "🔙Отменить":
        await state.update_data(price=message.text)
        data = await state.get_data()
        await message.answer(
            f"Отправьте фотографию для <b>{data['title']}</b>:",
            reply_markup=reply_kb.cancel_keyboard,
            parse_mode="HTML"
        )
        await state.set_state(AdminCreateItemStates.create_image)
    else:
        await message.answer("Создание новой позиции отменено!", show_alert=True)
        await state.clear()
        await admin_products_handler(message)


@router.message(AdminCreateItemStates.create_image, F.photo)
async def create_process_photo(message: Message, state: FSMContext):
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except TelegramBadRequest:
        pass

    data = await state.get_data()
    photo = message.photo[-1]
    file_id = photo.file_id

    folder = "database/images"
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/{data['title'].replace(' ', '_')}_{message.from_user.id}.jpg"

    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, file_path)

    add_item(data['title'], data['description'], data['price'], file_path)

    await message.answer_photo(
        FSInputFile(file_path),
        caption=f"✅ Товар добавлен:\n\n📦 {data['title']}\n📝 {data['description']}\n💰 {data['price']}₽",
        reply_markup=reply_kb.admin_menu_products_keyboard,
        parse_mode="HTML"
    )
    await state.clear()


@router.message(F.text=="Удалить позицию из меню ❌")
async def delete_item_handler(message: Message, state: FSMContext):
    """Удаление товара"""
    if message.from_user.id != message.chat.id:
        return

    menu = get_menu()
    if not menu:  # Проверяем что меню не пустое
        await message.answer("⚠️ Меню временно недоступно")
        return

    await state.clear()
    await state.update_data(menu=menu, current_index=0, delete_item=True)
    await show_menu(message, state)


@router.message(F.text=="Заказы 📥")
@router.callback_query(F.data.startswith("requested_orders:"))
async def admin_orders_handler(message_or_cb, state: FSMContext):
    """Переход к заказам для АДМИНОВ"""
    orders = get_all_orders()
    if isinstance(message_or_cb, CallbackQuery):
        message = message_or_cb.message
        user_id = message_or_cb.from_user.id
        order_id = int(message_or_cb.data.split(":")[1])
        index = next((i for i, order in enumerate(orders) if order[0] == order_id), 0)

    else:
        message = message_or_cb
        user_id = message_or_cb.from_user.id
        index = 0
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    if user_id not in ADMINS_ID:
        return

    orders = get_all_orders()

    if not orders:
        await message.answer("Активных заказов сейчас нет.")
        return

    await state.update_data(orders=orders, current_index=index)
    await  show_all_orders(message, state)


async def show_all_orders(message_or_cb, state: FSMContext, is_navigation=False):
    data = await state.get_data()
    orders = data['orders']
    index = data['current_index']

    print(index)
    if index < 0 or index >= len(orders):
        await message_or_cb.answer("Ошибка отображения заказов.")
        return

    order = orders[index]
    order_id, user_id, items_json, status, total_price, created_at = order
    user = get_user(user_id)

    text = (f"<b><u>Заказ #{order_id}</u></b>\n\n"
            f"<u>Покупатель</u>: <b>{user[3]}</b>\n"
            f"<u>Номер телефона:</u> <b>{user[4]}</b>\n\n"
            f"<u>Итоговая цена:</u> <b>{total_price} рублей</b>\n"
            f"<u>Статус заказа:</u> <b>{status}</b>\n"
            f"<u>Дата и время заказа:</u>\n"
            f"<b>{created_at}</b>\n"
            f"__________________________________")

    kb = inline_kb.get_admin_all_orders_keyboard(order_id)
    await state.update_data(order_id=order_id)

    try:
        if is_navigation:
            await message_or_cb.edit_text(
                text,
                reply_markup=kb,
                parse_mode="HTML"
            )
        else:
            await message_or_cb.answer(
                text,
                reply_markup=kb,
                parse_mode="HTML"
            )
    except TelegramBadRequest:
        await message_or_cb.answer(
            text,
            reply_markup=kb,
            parse_mode="HTML"
        )


@router.callback_query(F.data.in_(["prev_order", "next_order"]))
async def navigate_all_orders(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data['current_index']
    orders = data['orders']

    if callback.data == "prev_order":
        index = (index - 1) % len(orders)
    else:
        index = (index + 1) % len(orders)

    await state.update_data(current_index=index)
    await show_all_orders(callback.message, state, is_navigation=True)
    await callback.answer()


@router.callback_query(F.data.startswith("switch_status:"))
async def switch_status_handler(callback: CallbackQuery, state: FSMContext):
    """Смена статуса заказов"""
    await callback.message.edit_text(f"Задайте новый статус заказа:", reply_markup=status_order_keyboard())


@router.callback_query(F.data.startswith("update_status:"))
async def process_switch_status(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order_id = data['order_id']
    status = ""

    if not order_id:
        await callback.answer("Ошибка: не удалось получить ID заказа.", show_alert=True)
        return

    status_key = callback.data.split("update_status:")[1]
    if status_key == "cook":
        status = "Заказа уже готовится🕚"
    elif status_key == "done":
        status = "Ваш заказ готов❤️"

    switch_status_order(order_id, status)
    orders = get_all_orders()

    await state.update_data(orders=orders)

    await show_all_orders(callback.message, state, is_navigation=True)
    await callback.answer(f"Статус заказа #{order_id} успешно изменен на {status}", show_alert=True)


@router.message(F.text == "🔙 В главное меню")
async def exit_admin_panel(message: Message):
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    if message.from_user.id not in ADMINS_ID:
        return

    await message.answer(
        "Вы вышли из админ-панели",
        reply_markup=reply_kb.main_keyboard
    )
