from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from utils.database import get_user_context, update_user_context


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(self, handler, event: Message, data: dict):
        # Создаем сессию для работы с базой данных
        async with self.sessionmaker() as session:
            data["db_session"] = session  # Добавляем сессию в контекст обработки события

            await self.on_pre_process_event(event, data)

            await handler(event, data)

    async def on_pre_process_event(self, event, data: dict):
        async with self.sessionmaker() as session:
            user_context = await get_user_context(session, event)

            if not user_context:
                return

            await update_user_context(user_context, event)
            await session.commit()
