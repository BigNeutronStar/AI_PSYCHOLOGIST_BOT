from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import DATABASE_URL
from utils.actions_json import ActionsJSON
from sqlalchemy import BigInteger

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    mood = Column(String, nullable=True)

    contexts = relationship("UserContext", back_populates="user")


class UserContext(Base):
    __tablename__ = "users_context"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)  # Внешний ключ на таблицу users
    context_data = Column(String, nullable=True)  # Контекст пользователя (например, JSON)
    created_at = Column(String, nullable=False)  # Время создания записи
    updated_at = Column(String, nullable=False)  # Время обновления записи

    # Связь с таблицей users
    user = relationship("User", back_populates="contexts")


# Настройка подключения к базе данных
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_user_and_context(user_data, message: Message):
    async with async_session() as session:
        try:
            # Начинаем транзакцию
            async with session.begin():
                # Создаем пользователя
                user = User(
                    user_id=message.from_user.id,
                    username=message.from_user.username,
                    name=user_data["name"],
                    age=int(user_data["age"]),
                    mood=user_data["mood"],
                )
                session.add(user)

                # Создаем контекст
                user_context = UserContext(
                    user_id=message.from_user.id,
                    context_data=ActionsJSON().to_json(),
                    created_at=str(datetime.now()),
                    updated_at=str(datetime.now())
                )
                session.add(user_context)

            # Коммит транзакции
            await session.commit()
        except Exception as e:
            # Откат транзакции в случае ошибки
            await session.rollback()
            raise e


async def get_user(session: AsyncSession, event):
    # Формируем запрос с использованием ORM
    stmt = select(User).where(User.user_id == event.from_user.id)
    result = await session.execute(stmt)
    user = result.scalars().first()  # User или None

    return user


async def get_user_context(session: AsyncSession, event):
    stmt = select(UserContext).where(UserContext.user_id == event.from_user.id)
    result = await session.execute(stmt)
    return result.scalars().first()  # Возвращает список контекстов пользователя


async def update_user_context(user_context, event):
    new_context_data = ActionsJSON.from_json(user_context.context_data)

    if isinstance(event, Message):
        if event.text.startswith('/'):
            new_context_data.add_command(event.text)
        else:
            new_context_data.add_message(event.text)
    else:
        new_context_data.add_command(event.data)

    user_context.context_data = new_context_data.to_json()
    user_context.updated_at = str(datetime.now())
