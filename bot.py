from aiogram import Dispatcher
from handlers.handlers import router  # Импортируем общий роутер из handlers.py
from utils.scheduler import start_scheduler
from config import bot

dp = Dispatcher()

# Регистрируем роутер
dp.include_router(router)

async def main():
    start_scheduler()  # Запуск планировщика (если используется)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
