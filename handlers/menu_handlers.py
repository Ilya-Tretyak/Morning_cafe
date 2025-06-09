from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN
from keyboards import inline_kb
from database.database import get_menu


router = Router()
bot = Bot(token=BOT_TOKEN)

@router.message(F.text=="Меню ☕️")
async def menu_handler(message: Message, state: FSMContext):
    menu = get_menu()
    if not menu:  # Проверяем что меню не пустое
        await message.answer("⚠️ Меню временно недоступно")
        return

    await state.set_state(None)
    await state.update_data(menu=menu, current_index=0)
    await show_menu(message, state)


async def show_menu(message: Message, state: FSMContext):
    try:
        await message.delete()
    except ValueError:
        pass

    data = await state.get_data()

    if 'menu' not in data or 'current_index' not in data:
        await message.answer("⚠️ Ошибка загрузки меню. Пожалуйста, откройте меню снова.")
        return

    menu = data['menu']
    menu_item = menu[data['current_index']]

    text = (f"<u>{menu_item[1]} </u>\n\n"
            f"<i>{menu_item[2]} </i>\n\n"
            f"<b>Цена: {menu_item[3]}</b>")

    try:
        await message.answer_photo(
                photo=FSInputFile(menu_item[4]),
                caption=text,
                reply_markup=inline_kb.get_menu_navigation_keyboard(menu_item[0]),
                parse_mode="HTML"
        )
    except FileNotFoundError:
        await message.answer(
            text=f"{text}\n\n⚠️ Фото не найдено",
            reply_markup=inline_kb.get_menu_navigation_keyboard(menu_item[0])
        )

@router.callback_query(F.data.in_(["prev_item", "next_item", "close_menu"]))
async def handle_user_navigation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if 'menu' not in data or 'current_index' not in data:
        await callback.answer("Меню не загружено. Откройте меню снова.", show_alert=True)
        await callback.message.delete()
        return

    current_index = data['current_index']
    menu = data['menu']

    if callback.data == "prev_item":
        new_index = max(0, current_index - 1)
    elif callback.data == "next_item":
        new_index = min(len(menu) - 1, current_index + 1)
    else:
        await callback.message.delete()
        await state.clear()
        return

    await state.update_data(current_index=new_index)


    await show_menu(callback.message, state)

    await callback.answer()