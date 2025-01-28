from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from states.generall_states import GeneralStates
from utils.langchain_api import detect_mood, generate_support_response, chat_with_gpt
from utils.keyboards import main_menu_buttons_texts
from aiogram.types import Message

router = Router()


# ----------------------
# Общий обработчик текстовых сообщений
# ----------------------

@router.message(GeneralStates.waiting_for_mood)
async def handle_general_mood(message: Message, state: FSMContext):
    mood = await detect_mood(message)
    await message.answer(f"Ваше настроение: {mood}")
    await state.clear()


@router.message(GeneralStates.waiting_for_support)
async def handle_general_mood(message: Message, state: FSMContext):
    response = await generate_support_response(message=message)
    await message.answer(response)
    await state.clear()


@router.message(
    F.text & ~F.text.startswith("/") & ~F.text.func(lambda text: text in main_menu_buttons_texts))
async def handle_general_message(message: Message):
    # Отправляем обёрнутое сообщение в модель
    print("==========>")
    response = await chat_with_gpt(message)

    # Отправляем ответ пользователю
    await message.answer(response)

