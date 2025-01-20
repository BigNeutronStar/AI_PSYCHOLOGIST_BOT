from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.registration import RegistrationStates
from states.feedback import FeedbackStates
from utils.langchain_api import detect_mood, generate_support_response, chat_with_gpt
from utils.keyboards import main_menu_keyboard, give_subscribe_inline_keyboard, relaxation_keyboard, self_help_keyboard, create_feedback_keyboard
from utils.registration import check_name, check_age
from utils.scheduler import subscribe_daily_reminder, unsubscribe_daily_reminder
from utils.database import create_user_and_context
from config import bot

# Создаем единый роутер
router = Router()

# Состояния пользователей
user_states = {}


# ----------------------
# Команда /start
# ----------------------
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
        await message.answer("Пожалуйста, введите возраст числом (от 1 до 120).")
        return

    await state.update_data(age=message.text)
    await message.answer("Какое у тебя настроение? (радость, грусть, тревога, злость, нейтральное)")
    await state.set_state(RegistrationStates.waiting_for_mood)


@router.message(RegistrationStates.waiting_for_mood)
async def process_mood(message: Message, state: FSMContext):
    await state.update_data(mood=message.text)
    user_data = await state.get_data()
    await message.answer(f"Спасибо, {user_data['name']}! Ты зарегистрирован.", reply_markup=main_menu_keyboard)

    await create_user_and_context(user_data, message)
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
        mood = await detect_mood(message)
        await message.answer(f"Ваше настроение: {mood}")
        user_states[message.from_user.id] = None
    else:
        await handle_general_message(message)



# ----------------------
# Команда /relax
# ----------------------
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
        mood = await detect_mood(message)
        response = await generate_support_response(mood=mood, message=message)
        await message.answer(response)
        user_states[message.from_user.id] = None
    else:
        await handle_general_message(message)

# ----------------------
# Общий обработчик текстовых сообщений
# ----------------------
@router.message(F.text & ~F.text.startswith("/"))
async def handle_general_message(message: Message):
    # Отправляем обёрнутое сообщение в модель
    response = await chat_with_gpt(message)

    # Отправляем ответ пользователю
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
    technique_name = subscribe_techniques.get("_".join(callback.data.split('_')[2:]))
    subscribe_daily_reminder(bot, chat_id, technique_name)
    await callback.message.answer(f"Вы подписаны на ежедневные напоминания для техники '{technique_name}'.",
                                  reply_markup=main_menu_keyboard)


@router.callback_query(F.data.startswith("unsubscribe_scheduler"))
async def unsubscribe_gratitude(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    technique_name = subscribe_techniques.get("_".join(callback.data.split('_')[2:]))
    unsubscribe_daily_reminder(chat_id, technique_name)
    await callback.message.answer(f"Вы отписались от ежедневных напоминаний для техники '{technique_name}'.",
                                  reply_markup=main_menu_keyboard)


@router.callback_query(F.data == "cancel_subscribe_scheduler")
async def cancel_subscription(callback: CallbackQuery):
    await callback.message.answer("🫡", reply_markup=main_menu_keyboard)


# ----------------------
# Команда /feedback
# ----------------------

# Вопросы для обратной связи
feedback_questions = [
    "Как вам качество ответов?",
    "Насколько бот был полезен в решении вашей проблемы?",
    "Как вы оцениваете скорость работы бота?",
    "Насколько дружелюбным вам показался бот?",
    "Порекомендуете ли вы этого бота своим друзьям?",
]


# Начало сбора отзывов
@router.message(Command("feedback"))
async def start_feedback(message: Message, state: FSMContext):
    # Очищаем состояние и данные перед началом
    await state.clear()

    # Инициализируем сбор отзывов
    await state.update_data(responses=[])
    await message.answer(feedback_questions[0], reply_markup=create_feedback_keyboard())
    await state.set_state(FeedbackStates.waiting_for_question_1)


# Обработка вопросов
@router.callback_query(FeedbackStates.waiting_for_question_1, F.data.startswith("feedback:"))
async def handle_feedback_question_1(callback: CallbackQuery, state: FSMContext):
    await process_feedback(callback, state, current_question=0, next_state=FeedbackStates.waiting_for_question_2)


@router.callback_query(FeedbackStates.waiting_for_question_2, F.data.startswith("feedback:"))
async def handle_feedback_question_2(callback: CallbackQuery, state: FSMContext):
    await process_feedback(callback, state, current_question=1, next_state=FeedbackStates.waiting_for_question_3)


@router.callback_query(FeedbackStates.waiting_for_question_3, F.data.startswith("feedback:"))
async def handle_feedback_question_3(callback: CallbackQuery, state: FSMContext):
    await process_feedback(callback, state, current_question=2, next_state=FeedbackStates.waiting_for_question_4)


@router.callback_query(FeedbackStates.waiting_for_question_4, F.data.startswith("feedback:"))
async def handle_feedback_question_4(callback: CallbackQuery, state: FSMContext):
    await process_feedback(callback, state, current_question=3, next_state=FeedbackStates.waiting_for_question_5)


@router.callback_query(FeedbackStates.waiting_for_question_5, F.data.startswith("feedback:"))
async def handle_feedback_question_5(callback: CallbackQuery, state: FSMContext):
    await process_feedback(callback, state, current_question=4, next_state=None)


# Универсальная функция обработки отзывов
async def process_feedback(callback: CallbackQuery, state: FSMContext, current_question: int, next_state):
    # Извлекаем оценку
    rating = int(callback.data.split(":")[1])

    # Сохраняем ответ
    data = await state.get_data()
    data["responses"].append({"question": feedback_questions[current_question], "rating": rating})
    await state.update_data(responses=data["responses"])

    # Удаляем сообщение с кнопками
    await callback.message.delete()

    # Если есть следующий вопрос, задаем его
    if next_state:
        await callback.message.answer(feedback_questions[current_question + 1], reply_markup=create_feedback_keyboard())
        await state.set_state(next_state)
    else:
        # Завершаем сбор обратной связи
        feedback = await state.get_data()
        await callback.message.answer("Спасибо за ваш отзыв! Ваши оценки помогут нам стать лучше.")
        print(f"Отзывы пользователя {callback.from_user.id}: {feedback['responses']}")

        # Сбрасываем состояние
        await state.clear()

