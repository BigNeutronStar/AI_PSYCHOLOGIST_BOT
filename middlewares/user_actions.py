from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from utils.database import get_user


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(self, handler, event: Message, data: dict):
        # Создаем сессию для работы с базой данных
        async with self.sessionmaker() as session:
            data["db_session"] = session  # Добавляем сессию в контекст обработки события

            if isinstance(event, Message):
                await self.on_pre_process_message(event, data)
            elif isinstance(event, CallbackQuery):
                await self.on_pre_process_callback_query(event, data)

            await handler(event, data)

    async def on_pre_process_message(self, message: Message, data: dict):
        print(f"Processing message: {message.text}")

        async with self.sessionmaker() as session:
            user = await get_user(session, message)

            if not user:
                return

            user.actions = f"{user.actions or ''} | {message.text}"
            await session.commit()

    async def on_pre_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        # Логируем действия пользователя
        print(f"Processing callback query: {callback_query.data}")

        async with self.sessionmaker() as session:
            user = await get_user(session, callback_query)
            user.actions = f"{user.actions or ''} | {callback_query.data}"
            await session.commit()
