import logging

from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from handlers import command, registration_handlers, menu_handlers, basket_handlers, order_handlers, admin_handlers
import asyncio


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)

    dp.include_router(command.router)
    dp.include_router(registration_handlers.router)
    dp.include_router(menu_handlers.router)
    dp.include_router(basket_handlers.router)
    dp.include_router(order_handlers.router)
    dp.include_router(admin_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
