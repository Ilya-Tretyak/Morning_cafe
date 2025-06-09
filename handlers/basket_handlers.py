from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN
from keyboards import inline_kb
from ustils.state import OrderStates
from database.database import get_sizes, get_additives


router = Router()
bot = Bot(token=BOT_TOKEN)


@router.callback_query(F.data.startswith("add_to_order:"))
async def add_to_basket(callback: CallbackQuery, state: FSMContext):
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
    await state.update_data(additives_id=int(callback.data.split(":")[1]))
    additives = get_additives()
    sizes = get_sizes()
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
    pass