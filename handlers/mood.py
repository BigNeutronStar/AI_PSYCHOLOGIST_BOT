from aiogram import Router, F
from aiogram.types import Message
from utils.langchain import detect_mood
from utils.keyboards import main_menu_keyboard

router = Router()

@router.message(F.text == "Определить настроение")
async def handle_mood(message: Message):
    await message.answer("Напиши, что у тебя на душе, и я определю твое настроение.")

@router.message(F.text)
async def detect_user_mood(message: Message):
    # Проверяем, что это не команда или кнопка
    if message.text not in ["Определить настроение", "Рекомендации по релаксации", "Психологическая поддержка", "Техники самопомощи", "Финальная анкета"]:
        mood = await detect_mood(message.text)
        await message.answer(f"Ваше настроение: {mood}", reply_markup=main_menu_keyboard)