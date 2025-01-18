import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

# Настраиваем базовое логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class LoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        # Логируем входящее событие
        logging.info(f"Получено событие: {event}")
        # Передаем управление следующему обработчику
        result = await handler(event, data)
        # Логируем результат обработки (при необходимости)
        logging.info(f"Результат обработки: {result}")
        return result
