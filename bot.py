from aiogram import Dispatcher
from handlers import router
from utils.scheduler import start_scheduler  # Импорт функции для запуска планировщика
from config import bot

dp = Dispatcher()

dp.include_router(router)


async def main():
    start_scheduler()  # Запуск планировщика
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
