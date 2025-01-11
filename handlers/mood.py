from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.langchain import detect_mood
from utils.keyboards import main_menu_keyboard

router = Router()

@router.message(Command("mood"))
async def handle_mood(message: Message):
    await message.answer("Напиши, что у тебя на душе, и я определю твое настроение.")

@router.message(F.text & ~F.text.startswith("/"))  # Игнорируем команды
async def detect_user_mood(message: Message):
    mood = await detect_mood(message.text)
    await message.answer(f"Ваше настроение: {mood}", reply_markup=main_menu_keyboard)