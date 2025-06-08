from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from handlers import command, registration_handlers, menu_handlers
import asyncio


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(command.router)
    dp.include_router(registration_handlers.router)
    dp.include_router(menu_handlers.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
