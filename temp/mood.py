from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.langchain import detect_mood

router = Router()

# Состояния пользователей (временное решение, лучше использовать базу данных или Redis)
user_states = {}

@router.message(Command("mood"))  # Обрабатываем команду /mood
async def handle_mood(message: Message):
    user_states[message.from_user.id] = "waiting_for_mood"  # Устанавливаем состояние пользователя
    await message.answer("Напиши, что у тебя на душе, и я определю твое настроение.")

@router.message(F.text & ~F.text.startswith("/"))  # Обрабатываем текстовые сообщения
async def detect_user_mood(message: Message):
    # Проверяем состояние пользователя
    if user_states.get(message.from_user.id) == "waiting_for_mood":
        # Определяем настроение
        mood = await detect_mood(message.text)
        await message.answer(f"Ваше настроение: {mood}")
        user_states[message.from_user.id] = None  # Сбрасываем состояние
    else:
        # Игнорируем сообщения вне контекста
        return
