from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from utils.keyboards import main_menu_keyboard

router = Router()

relaxation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дыхательные упражнения", callback_data="breathing")],
    [InlineKeyboardButton(text="Медитация", callback_data="meditation")],
    [InlineKeyboardButton(text="Прогрессивная релаксация", callback_data="progressive")]
])

@router.message(F.text == "Рекомендации по релаксации")
async def suggest_relaxation(message: Message):
    await message.answer("Выбери технику релаксации:", reply_markup=relaxation_keyboard)

@router.callback_query(F.data == "breathing")
async def breathing_exercise(callback: CallbackQuery):
    await callback.message.answer("Техника '4-7-8': Вдохните на 4 секунды, задержите дыхание на 7 секунд, выдохните на 8 секунд.", reply_markup=main_menu_keyboard)

@router.callback_query(F.data == "meditation")
async def meditation_exercise(callback: CallbackQuery):
    await callback.message.answer("Медитация: Сядьте удобно, закройте глаза и сосредоточьтесь на своем дыхании. Дышите медленно и глубоко.", reply_markup=main_menu_keyboard)

@router.callback_query(F.data == "progressive")
async def progressive_relaxation(callback: CallbackQuery):
    await callback.message.answer("Прогрессивная релаксация: Напрягайте и расслабляйте мышцы по очереди, начиная с ног и заканчивая лицом.", reply_markup=main_menu_keyboard)