from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN
from keyboards import inline_kb


router = Router()
bot = Bot(token=BOT_TOKEN)

@router.message(F.text=="Корзина 🗑️")
async def basket_handler(message: Message):
    pass