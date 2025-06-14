from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN
from keyboards import inline_kb
from database.database import get_menu, delete_item

router = Router()
bot = Bot(token=BOT_TOKEN)

@router.message(F.text=="Меню ☕️")
async def menu_handler(message: Message, state: FSMContext):
    """Проверка и получение меню"""
    menu = get_menu()
    if not menu:  # Проверяем что меню не пустое
        await message.answer("⚠️ Меню временно недоступно")
        return

    await state.clear()
    await state.update_data(menu=menu, current_index=0, delete_item=False)
    await show_menu(message, state)


async def show_menu(message_or_callback, state: FSMContext, is_navigation=False):
    """Отображение меню для пользователя"""
    data = await state.get_data()
    menu = data['menu']
    menu_item = menu[data['current_index']]

    text = (f"<u>{menu_item[1]} </u>\n\n"
            f"<i>{menu_item[2]} </i>\n\n"
            f"<b>Цена: {menu_item[3]} руб.</b>")

    if data['delete_item'] is False:
        kb = inline_kb.get_menu_navigation_keyboard(menu_item[0])
    else:
        kb = inline_kb.delete_item_navigation_keyboard(menu_item[0])

    try:
        file = FSInputFile(menu_item[4])
        if is_navigation:
            await message_or_callback.edit_media(
                media=InputMediaPhoto(
                    media=file,
                    caption=text,
                    parse_mode="HTML"
                ),
                reply_markup=kb
            )
        else:
            try:
                await message_or_callback.delete()
            except TelegramBadRequest:
                pass
            await message_or_callback.answer_photo(
                photo=file,
                caption=text,
                reply_markup=kb,
                parse_mode="HTML"
            )
    except FileNotFoundError:
        if is_navigation:
            await message_or_callback.message.edit_caption(
                caption=f"{text}\n\n⚠️ Фото не найдено",
                reply_markup=kb,
                parse_mode="HTML"
            )
        else:
            await message_or_callback.answer(
                text=f"{text}\n\n⚠️ Фото не найдено",
                reply_markup=kb
            )

@router.callback_query(F.data.in_(["prev_item", "next_item", "close_menu", "delete_item"]))
async def handle_user_navigation(callback: CallbackQuery, state: FSMContext):
    """Реализация навигации"""
    data = await state.get_data()

    if 'menu' not in data or 'current_index' not in data:
        await callback.answer("Меню не загружено. Откройте меню снова.", show_alert=True)
        await callback.message.delete()
        return

    current_index = data['current_index']
    menu = data['menu']

    if callback.data == "prev_item":
        new_index = (current_index - 1) % len(menu)
    elif callback.data == "next_item":
        new_index = (current_index + 1) % len(menu)
    elif callback.data == "delete_item":
        delete_item(menu[current_index][0])
        await callback.answer(f"Позиция удалена из меню!", show_alert=True)
        menu = get_menu()
        await state.update_data(menu=menu)
        new_index = (current_index - 1) % len(menu)
    else:
        await callback.message.delete()
        await state.clear()
        return

    await state.update_data(current_index=new_index)
    await show_menu(callback.message, state, is_navigation=True)
    await callback.answer()