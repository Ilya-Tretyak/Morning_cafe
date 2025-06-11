from idlelib.undo import Command

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN, ADMINS_ID


router = Router()
bot = Bot(token=BOT_TOKEN)


@router.message(F.text=="Товары 🛒")
async def admin_products_handler(message: Message):
    if message.from_user.id in ADMINS_ID:
        print("Done")
    else:
        print("None")
    pass


@router.message(F.text=="Заказы 📥")
async def admin_orders_handler(message: Message):
    if message.from_user.id in ADMINS_ID:
        print("Done")
    else:
        print("None")
    pass


@router.message(F.text=="Выручка 💸")
async def admin_cash_handler(message: Message):
    if message.from_user.id in ADMINS_ID:
        print("Done")
    else:
        print("None")
    pass
