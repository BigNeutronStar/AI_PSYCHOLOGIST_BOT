from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.langchain import generate_support_response, detect_mood
from utils.keyboards import main_menu_keyboard

router = Router()


@router.message(Command("support"))
async def handle_support(message: Message):
    await message.answer("Напиши, что тебя беспокоит, и я постараюсь поддержать тебя.")
    return  # Добавьте эту строку


@router.message(F.text)
async def generate_support(message: Message):
    mood = await detect_mood(message)
    response = await generate_support_response(mood=mood, message=message)
    await message.answer(response, reply_markup=main_menu_keyboard)
