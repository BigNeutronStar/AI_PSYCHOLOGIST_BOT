from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from utils.keyboards import main_menu_keyboard

from utils.check_registration import check_age, check_name

router = Router()

class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_mood = State()

@router.message(Command("start"))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Привет! Давай зарегистрируемся. Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.waiting_for_name)

@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if not check_name(message.text):
        await message.answer("Пожалуйста, введите имя, используя только буквы.")
        return

    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(RegistrationStates.waiting_for_age)

@router.message(RegistrationStates.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    if not check_age(message.text):
        await message.answer("Пожалуйста, введите возраст числом.")
        return

    await state.update_data(age=message.text)
    await message.answer("Какое у тебя настроение? (радость, грусть, тревога, злость, нейтральное)")
    await state.set_state(RegistrationStates.waiting_for_mood)

@router.message(RegistrationStates.waiting_for_mood)
async def process_mood(message: Message, state: FSMContext):
    await state.update_data(mood=message.text)
    user_data = await state.get_data()
    await message.answer(f"Спасибо, {user_data['name']}! Ты зарегистрирован.", reply_markup=main_menu_keyboard)
    await state.clear()