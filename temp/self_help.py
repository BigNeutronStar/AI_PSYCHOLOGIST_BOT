from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from utils.keyboards import give_subscribe_inline_keyboard


router = Router()

self_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дневник благодарности", callback_data="gratitude")],
    [InlineKeyboardButton(text="Упражнение 'Пять чувств'", callback_data="five_senses")]
])


@router.message(Command("self_help"))
async def suggest_self_help(message: Message):
    await message.answer("Выбери технику самопомощи:", reply_markup=self_help_keyboard)
    return  # Добавьте эту строку


@router.callback_query(F.data == "gratitude")
async def gratitude_journal(callback: CallbackQuery):
    await callback.message.answer("Запиши 3 вещи, за которые ты благодарен.",
                                  reply_markup=give_subscribe_inline_keyboard("gratitude"))


@router.callback_query(F.data == "five_senses")
async def five_senses_exercise(callback: CallbackQuery):
    await callback.message.answer("Назови 5 вещей, которые ты видишь, 4 вещи, которые ты слышишь, 3 вещи, которые ты чувствуешь, 2 вещи, которые ты ощущаешь на вкус, и 1 вещь, которую ты чувствуешь запахом.",
                                  reply_markup=give_subscribe_inline_keyboard("five_senses"))
