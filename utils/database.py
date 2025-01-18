from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    mood = Column(String, nullable=True)
    actions = Column(String, nullable=True)


# Настройка подключения к базе данных
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_user(user_data, message: Message):
    async with async_session() as session:
        user = User(
            chat_id=message.from_user.id,
            username=message.from_user.username,
            name=user_data["name"],
            age=int(user_data["age"]),
            mood=user_data["mood"],
            actions=""
        )
        session.add(user)
        await session.commit()
    return user


async def get_user(session: AsyncSession, event):
    # Формируем запрос с использованием ORM
    stmt = select(User).where(User.chat_id == event.from_user.id)
    result = await session.execute(stmt)
    user = result.scalars().first()  # User или None

    return user
