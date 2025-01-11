from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router = Router()

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()

@router.message(F.text == "Финальная анкета")
async def start_feedback(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, расскажи, как тебе наш бот?")
    await state.set_state(FeedbackStates.waiting_for_feedback)

@router.message(FeedbackStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    await message.answer("Спасибо за твой отзыв!", reply_markup=main_menu_keyboard)
    await state.clear()