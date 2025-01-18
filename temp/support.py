from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.langchain import generate_support_response, detect_mood

router = Router()

@router.message(Command("support"))  # Обрабатываем только команду /support
async def handle_support(message: Message):
    await message.answer("Напиши, что тебя беспокоит, и я постараюсь поддержать тебя.")

@router.message(F.text & ~F.text.startswith("/"))  # Обрабатываем только сообщения после /support
async def generate_support(message: Message):
    mood = await detect_mood(message.text)  # Определяем настроение пользователя
    response = await generate_support_response(mood=mood, message=message.text)
    await message.answer(response)
