from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.database import User


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(self, handler, event: Message, data: dict):
        # Создаем сессию для работы с базой данных
        print(event)
        async with self.sessionmaker() as session:
            data["db_session"] = session  # Добавляем сессию в контекст обработки события

            if isinstance(event, Message):
                await self.on_pre_process_message(event, data)
            elif isinstance(event, CallbackQuery):
                await self.on_pre_process_callback_query(event, data)

                # Передаём обработку дальше
            await handler(event, data)

    async def on_pre_process_message(self, message: Message, data: dict):
        print(f"Processing message: {message.text}")
        # Логируем действия пользователя
        async with self.sessionmaker() as session:
            user = await self.get_or_create_user(session, message.from_user)
            user.actions = f"{user.actions or ''} | {message.text}"
            await session.commit()

    async def on_pre_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        # Логируем действия пользователя
        print(f"Processing callback query: {callback_query.data}")
        async with self.sessionmaker() as session:
            user = await self.get_or_create_user(session, callback_query.from_user)
            user.actions = f"{user.actions or ''} | {callback_query.data}"
            await session.commit()

    @staticmethod
    async def get_or_create_user(session: AsyncSession, user_data):
        # Формируем запрос с использованием ORM
        stmt = select(User).where(User.chat_id == user_data.id)
        result = await session.execute(stmt)
        user = result.scalars().first()  # Получаем объект User или None

        # Отладочный вывод
        print("===>", user)

        if not user:
            user = User(
                chat_id=user_data.id,
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                actions=""
            )
            session.add(user)
        return user
