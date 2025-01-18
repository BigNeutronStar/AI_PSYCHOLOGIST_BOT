from aiogram import Dispatcher

from handlers.handlers import router  # Импортируем общий роутер из handlers.py

from utils.scheduler import start_scheduler
from config import bot
from middlewares.user_actions import DatabaseMiddleware
from middlewares.check_registration import CheckRegistrationMiddleware
from utils.database import async_session, init_db

dp = Dispatcher()

dp.message.middleware(CheckRegistrationMiddleware(async_session))
dp.message.middleware(DatabaseMiddleware(async_session))
dp.callback_query.middleware(DatabaseMiddleware(async_session))
dp.include_router(router)


async def main():
    start_scheduler()  # Запуск планировщика (если используется)
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
