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
    await message.delete()
    await bot.delete_message(message.chat.id, message.message_id - 1)

    menu = get_menu()
    await state.update_data(menu=menu, current_index=0)
    await message.answer("📖 Меню 📖")
    await show_menu(message, state)


async def show_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    menu = data['menu']
    menu_item = menu[data['current_index']]
    text = (f"<u>{menu_item[1]}</u>\n\n"
            f"<i>{menu_item[2]}</i>\n"
            f"<b>{menu_item[3]}</b>")

    try:
        await message.answer_photo(
            photo=FSInputFile(menu_item[4]),
            caption=text,
            reply_markup=inline_kb.menu_navigation,
            parse_mode="HTML"
        )
    except FileNotFoundError:
        await message.answer(
            text=f"{text}\n\n⚠️ Фото не найдено",
        )

@router.callback_query(F.data.in_(["prev_item", "next_item", "close_menu"]))
async def handle_user_navigation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
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

    await callback.message.delete()
    await show_menu(callback.message, state)

    await callback.answer()