from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from utils.database import get_user
from aiogram.fsm.context import FSMContext


class CheckRegistrationMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(self, handler, message: Message, data: dict):
        async with self.sessionmaker() as session:
            user = await get_user(session, message)

            state: FSMContext = data["state"]
            current_state = await state.get_state()

            if user:
                if await self.is_registered_user_try_start(user, message):
                    return
                return await handler(message, data)

            if self.is_in_registration(message, current_state):
                return await handler(message, data)

            if await self.need_to_register(message, user, current_state):
                return

    @staticmethod
    def is_in_registration(message, current_state):
        if message.text == '/start':
            return True

        if current_state:
            return True

        return False

    @staticmethod
    async def need_to_register(message, user, current_state):
        if not user and not current_state:
            await message.answer(
                "Вам нужно зарегистрироваться, чтобы начать использовать бота. Используйте /start для начала.")
            return True
        return False

    @staticmethod
    async def is_registered_user_try_start(user, message):
        if user and message.text == '/start':
            await message.answer("Вы уже зарегистрированы и можете пользоваться ботом ;)")
            return True
        return False



