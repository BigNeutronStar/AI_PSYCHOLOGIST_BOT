from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.langchain import detect_mood, generate_support_response, chat_with_gpt
from utils.keyboards import main_menu_keyboard, give_subscribe_inline_keyboard
from utils.check_registration import check_name, check_age
from utils.scheduler import subscribe_daily_reminder, unsubscribe_daily_reminder
from config import bot

# Создаем единый роутер
router = Router()

# Хранилище состояний пользователя
user_states = {}

# ----------------------
# Команда /start
# ----------------------
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

# ----------------------
# Команда /mood
# ----------------------
@router.message(Command("mood"))
async def handle_mood(message: Message):
    user_states[message.from_user.id] = "waiting_for_mood"
    await message.answer("Напиши, что у тебя на душе, и я определю твое настроение.")

@router.message(F.text & ~F.text.startswith("/"))
async def detect_user_mood(message: Message):
    if user_states.get(message.from_user.id) == "waiting_for_mood":
        mood = await detect_mood(message.text)
        await message.answer(f"Ваше настроение: {mood}")
        user_states[message.from_user.id] = None
    else:
        response = await chat_with_gpt(message.text)
        await message.answer(response)

# ----------------------
# Команда /relax
# ----------------------
relaxation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дыхательные упражнения", callback_data="breathing")],
    [InlineKeyboardButton(text="Медитация", callback_data="meditation")],
    [InlineKeyboardButton(text="Прогрессивная релаксация", callback_data="progressive")]
])

@router.message(Command("relax"))
async def suggest_relaxation(message: Message):
    await message.answer("Выбери технику релаксации:", reply_markup=relaxation_keyboard)

@router.callback_query(F.data == "breathing")
async def breathing_exercise(callback: CallbackQuery):
    await callback.message.answer("Техника '4-7-8': Вдохните на 4 секунды, задержите дыхание на 7 секунд, выдохните на 8 секунд.",
                                  reply_markup=give_subscribe_inline_keyboard('breathing'))

@router.callback_query(F.data == "meditation")
async def meditation_exercise(callback: CallbackQuery):
    await callback.message.answer("Медитация: Сядьте удобно, закройте глаза и сосредоточьтесь на своем дыхании. Дышите медленно и глубоко.",
                                  reply_markup=give_subscribe_inline_keyboard('meditation'))

@router.callback_query(F.data == "progressive")
async def progressive_relaxation(callback: CallbackQuery):
    await callback.message.answer("Прогрессивная релаксация: Напрягайте и расслабляйте мышцы по очереди, начиная с ног и заканчивая лицом.",
                                  reply_markup=give_subscribe_inline_keyboard("progressive"))

# ----------------------
# Команда /self_help
# ----------------------
self_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дневник благодарности", callback_data="gratitude")],
    [InlineKeyboardButton(text="Упражнение 'Пять чувств'", callback_data="five_senses")]
])

@router.message(Command("self_help"))
async def suggest_self_help(message: Message):
    await message.answer("Выбери технику самопомощи:", reply_markup=self_help_keyboard)

@router.callback_query(F.data == "gratitude")
async def gratitude_journal(callback: CallbackQuery):
    await callback.message.answer("Запиши 3 вещи, за которые ты благодарен.",
                                  reply_markup=give_subscribe_inline_keyboard("gratitude"))

@router.callback_query(F.data == "five_senses")
async def five_senses_exercise(callback: CallbackQuery):
    await callback.message.answer("Назови 5 вещей, которые ты видишь, 4 вещи, которые ты слышишь, 3 вещи, которые ты чувствуешь, 2 вещи, которые ты ощущаешь на вкус, и 1 вещь, которую ты чувствуешь запахом.",
                                  reply_markup=give_subscribe_inline_keyboard("five_senses"))

# ----------------------
# Команда /support
# ----------------------
@router.message(Command("support"))
async def handle_support(message: Message):
    user_states[message.from_user.id] = "waiting_for_support"
    await message.answer("Напиши, что тебя беспокоит, и я постараюсь поддержать тебя.")

@router.message(F.text & ~F.text.startswith("/"))
async def generate_support(message: Message):
    if user_states.get(message.from_user.id) == "waiting_for_support":
        mood = await detect_mood(message.text)
        response = await generate_support_response(mood=mood, message=message.text)
        await message.answer(response)
        user_states[message.from_user.id] = None
    else:
        response = await chat_with_gpt(message.text)
        await message.answer(response)

# ----------------------
# Подписка / отписка
# ----------------------
subscribe_techniques = {
    "gratitude": "Дневник благодарности",
    "five_senses": "5 чувств",
    "breathing": "4-7-8",
    "meditation": "Медитация",
    "progressive": "Прогрессивная релаксация",
}

@router.callback_query(F.data.startswith("subscribe_scheduler"))
async def subscribe_gratitude(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    technique_name = subscribe_techniques.get(callback.data.split('_')[2])
    subscribe_daily_reminder(bot, chat_id, technique_name)
    await callback.message.answer(f"Вы подписаны на ежедневные напоминания для техники '{technique_name}'.",
                                  reply_markup=main_menu_keyboard)

@router.callback_query(F.data.startswith("unsubscribe_scheduler"))
async def unsubscribe_gratitude(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    technique_name = subscribe_techniques.get(callback.data.split('_')[2])
    unsubscribe_daily_reminder(chat_id, technique_name)
    await callback.message.answer(f"Вы отписались от ежедневных напоминаний для техники '{technique_name}'.",
                                  reply_markup=main_menu_keyboard)

@router.callback_query(F.data == "cancel_subscribe_scheduler")
async def cancel_subscription(callback: CallbackQuery):
    await callback.message.answer("🫡", reply_markup=main_menu_keyboard)
