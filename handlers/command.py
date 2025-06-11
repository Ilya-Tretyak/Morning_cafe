from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from config.settings import BOT_TOKEN, ADMINS_ID
from keyboards import reply_kb
from database.database import is_user_registered
from ustils.state import RegistrationStates


router = Router()
bot = Bot(token=BOT_TOKEN)

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    if is_user_registered(message.from_user.id):
        await message.answer_photo(
            photo=FSInputFile("database/images/dopping.jpg"),
            caption=f"Добро пожаловать в Morning Cup ☕️\n\n",
            reply_markup=reply_kb.main_keyboard
        )
    else:
        await state.set_state(RegistrationStates.full_name)
        await message.answer(
            f"Чтобы совершать заказы давайте познакомимся😉",
            reply_markup=reply_kb.start_register_keyboard
        )


@router.message(Command("admin"))
async def admin_handler(message: Message):
    if message.from_user.id in ADMINS_ID:
        await message.answer("Админ-панель:", reply_markup=reply_kb.admin_menu_keyboard)
    else:
        await message.answer(
            "К сожалению у вам нет доступа к админ-панели! Посмотрим меню?",
            reply_markup=reply_kb.main_keyboard
        )
