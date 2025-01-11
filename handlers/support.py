from aiogram import Router, F
from aiogram.types import Message
from utils.langchain import generate_support_response
from utils.keyboards import main_menu_keyboard

router = Router()

@router.message(F.text == "Психологическая поддержка")
async def handle_support(message: Message):
    await message.answer("Напиши, что тебя беспокоит, и я постараюсь поддержать тебя.")

@router.message(F.text)
async def generate_support(message: Message):
    # Проверяем, что это не команда или кнопка
    if message.text not in ["Определить настроение", "Рекомендации по релаксации", "Психологическая поддержка", "Техники самопомощи", "Финальная анкета"]:
        mood = "нейтральное"  # Можно заменить на вызов detect_mood
        response = await generate_support_response(mood=mood, message=message.text)
        await message.answer(response, reply_markup=main_menu_keyboard)