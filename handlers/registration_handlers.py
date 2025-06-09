from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config.settings import BOT_TOKEN
from keyboards import reply_kb
from database.database import add_user
from ustils.state import RegistrationStates

router = Router()
bot = Bot(token=BOT_TOKEN)


@router.message(F.text=="Зарегистрироваться✍️", RegistrationStates.full_name)
async def full_name_handler(message: Message, state: FSMContext):
    """Начало регистрации -> ввод имени"""
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

    await message.answer(
        f"Введите свое имя:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationStates.phone_number)


@router.message(RegistrationStates.phone_number)
async def phone_number_handler(message: Message, state: FSMContext):
    """Получение номера телефона"""
    await state.update_data(full_name=message.text)

    await message.delete()
    await bot.delete_message(message.chat.id, message.message_id - 1)

    await message.answer(
        "Для связи с вами, введите свой номер телефона📱:"
    )
    await state.set_state(RegistrationStates.confirm)


@router.message(RegistrationStates.confirm)
async def confirm_handler(message: Message, state: FSMContext):
    """Проверка введенных данных"""
    await state.update_data(phone_number=message.text)

    await message.delete()
    await bot.delete_message(message.chat.id, message.message_id - 1)

    data = await state.get_data()
    print(data)
    await message.answer(
        f"Все верно?🧐\n\n"
        f"Имя: {data['full_name']}\n"
        f"Номер телефона: {data['phone_number']}",
        reply_markup=reply_kb.yes_or_no_keyboard
    )
    await state.set_state(RegistrationStates.complete)


@router.message(F.text=="Да✅", RegistrationStates.complete)
async def complete_handler(message: Message, state: FSMContext):
    """Завершение регистрации"""
    await message.delete()
    await bot.delete_message(message.chat.id, message.message_id - 1)

    data = await state.get_data()
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = data['full_name']
    phone_number = data['phone_number']
    add_user(user_id, username, full_name, phone_number)
    await message.answer(
        f"{full_name}, вы успешно зарегистрировались!",
        reply_markup=reply_kb.main_keyboard
    )
    await state.clear()


@router.message(F.text == "Нет❌", RegistrationStates.complete)
async def not_register_handler(message: Message, state: FSMContext):
    """Переход в начало регистрации"""
    await message.delete()
    await bot.delete_message(message.chat.id, message.message_id - 1)

    await message.answer(
        f"Давайте попробуем еще раз:\n"
        f"Введите свое имя:"
    )
    await state.set_state(RegistrationStates.phone_number)