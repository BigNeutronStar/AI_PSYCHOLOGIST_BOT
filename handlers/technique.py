import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from states.techniques_states import GratitudeStates, FiveSensesStates
from utils.keyboards import main_menu_keyboard, give_start_technique_keyboard, give_subscribe_inline_keyboard, \
    relaxation_keyboard, self_help_keyboard, feelings_keyboard
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

# Создаем единый роутер
router = Router()


# ----------------------
# Команда /relax
# ----------------------
@router.message(Command("relax"))
@router.message(F.text == "Релакс")
async def suggest_relaxation(message: Message):
    await message.answer("Выбери технику релаксации:", reply_markup=relaxation_keyboard)


@router.callback_query(F.data == "breathing")
async def breathing_exercise(callback: CallbackQuery):
    await callback.message.answer(
        "Техника '4-7-8': Вдохните на 4 секунды, задержите дыхание на 7 секунд, выдохните на 8 секунд.",
        reply_markup=give_start_technique_keyboard("breathing"))


@router.callback_query(F.data == "start_breathing")
async def start_breathing(callback: CallbackQuery, state: FSMContext):
    await state.update_data(technique="breathing")

    await callback.message.answer("Вдохните на 4 секунды...")
    await asyncio.sleep(4)
    await callback.message.answer("Задержите дыхание на 7 секунд...")
    await asyncio.sleep(7)
    await callback.message.answer("Выдохните на 8 секунд...")
    await asyncio.sleep(8)
    await callback.message.answer("Как вы себя чувствуете?", reply_markup=feelings_keyboard)


@router.callback_query(F.data == "meditation")
async def meditation_exercise(callback: CallbackQuery):
    await callback.message.answer(
        "Медитация: Сядьте удобно, закройте глаза и сосредоточьтесь на своем дыхании. Дышите медленно и глубоко.",
        reply_markup=give_start_technique_keyboard("meditation")
    )


@router.callback_query(F.data == "start_meditation")
async def start_meditation(callback: CallbackQuery, state: FSMContext):
    await state.update_data(technique="meditation")
    await callback.message.answer("Сосредоточьтесь на дыхании... Через минуту я спрошу о вашем самочувствии")
    await asyncio.sleep(60)  # 1 минута медитации
    await callback.message.answer("Как вы себя чувствуете?", reply_markup=feelings_keyboard)


@router.callback_query(F.data == "progressive")
async def progressive_relaxation(callback: CallbackQuery):
    # Удаляем старое сообщение с кнопками

    # Отправляем новое сообщение
    await callback.message.answer(
        "Прогрессивная релаксация: Напрягайте и расслабляйте мышцы по очереди, начиная с ног и заканчивая лицом.",
        reply_markup=give_subscribe_inline_keyboard("progressive")
    )


# ----------------------
# Команда /self_help
# ----------------------
@router.message(Command("self_help"))
@router.message(F.text == "Успокоить себя самостоятельно")
async def suggest_self_help(message: Message):
    await message.answer("Выбери технику самопомощи:", reply_markup=self_help_keyboard)


@router.callback_query(F.data == "gratitude")
async def gratitude_journal(callback: CallbackQuery):
    await callback.message.answer(
        "Запиши 3 вещи, за которые ты благодарен.",
        reply_markup=give_start_technique_keyboard("gratitude")
    )


# Хендлер для техники благодарности
@router.callback_query(F.data == "start_gratitude")
async def start_gratitude(callback: CallbackQuery, state: FSMContext):
    await state.update_data(technique="gratitude")
    await callback.message.answer("Напишите первую вещь, за которую вы благодарны:")
    await state.set_state(GratitudeStates.first)


@router.message(GratitudeStates.first)
async def gratitude_first(message: Message, state: FSMContext):
    await state.update_data(first_gratitude=message.text)
    await message.answer("Напишите вторую вещь, за которую вы благодарны:")
    await state.set_state(GratitudeStates.second)


@router.message(GratitudeStates.second)
async def gratitude_second(message: Message, state: FSMContext):
    await state.update_data(second_gratitude=message.text)
    await message.answer("Напишите третью вещь, за которую вы благодарны:")
    await state.set_state(GratitudeStates.third)


@router.message(GratitudeStates.third)
async def gratitude_third(message: Message, state: FSMContext):
    await state.update_data(third_gratitude=message.text)
    data = await state.get_data()
    await message.answer(
        f"Спасибо! Вы записали:\n"
        f"1. {data['first_gratitude']}\n"
        f"2. {data['second_gratitude']}\n"
        f"3. {data['third_gratitude']}\n"
        f"Как вы себя чувствуете?",
        reply_markup=feelings_keyboard
    )


@router.callback_query(F.data == "five_senses")
async def five_senses_exercise(callback: CallbackQuery):
    await callback.message.answer(
        "Назови 5 вещей, которые ты видишь, 4 вещи, которые ты слышишь, 3 вещи, которые ты чувствуешь, "
        "2 вещи, которые ты ощущаешь на вкус, и 1 вещь, которую ты чувствуешь запахом.",
        reply_markup=give_start_technique_keyboard("five_senses")
    )


# Хендлер для техники 5 органов чувств
@router.callback_query(F.data == "start_five_senses")
async def start_five_senses(callback: CallbackQuery, state: FSMContext):
    await state.update_data(technique="five_senses")
    await callback.message.answer("Назовите 5 вещей, которые вы видите:")
    await state.set_state(FiveSensesStates.see)


@router.message(FiveSensesStates.see)
async def five_senses_see(message: Message, state: FSMContext):
    await state.update_data(see=message.text)
    await message.answer("Назовите 4 вещи, которые вы слышите:")
    await state.set_state(FiveSensesStates.hear)


@router.message(FiveSensesStates.hear)
async def five_senses_hear(message: Message, state: FSMContext):
    await state.update_data(hear=message.text)
    await message.answer("Назовите 3 вещи, которые вы чувствуете:")
    await state.set_state(FiveSensesStates.feel)


@router.message(FiveSensesStates.feel)
async def five_senses_feel(message: Message, state: FSMContext):
    await state.update_data(feel=message.text)
    await message.answer("Назовите 2 вещи, которые вы ощущаете на вкус:")
    await state.set_state(FiveSensesStates.taste)


@router.message(FiveSensesStates.taste)
async def five_senses_taste(message: Message, state: FSMContext):
    await state.update_data(taste=message.text)
    await message.answer("Назовите 1 вещь, которую вы чувствуете запахом:")
    await state.set_state(FiveSensesStates.smell)


@router.message(FiveSensesStates.smell)
async def five_senses_smell(message: Message, state: FSMContext):
    await state.update_data(smell=message.text)
    data = await state.get_data()
    await message.answer(
        f"Спасибо! Вы назвали:\n"
        f"5 вещей, которые видите: {data['see']}\n"
        f"4 вещи, которые слышите: {data['hear']}\n"
        f"3 вещи, которые чувствуете: {data['feel']}\n"
        f"2 вещи, которые ощущаете на вкус: {data['taste']}\n"
        f"1 вещь, которую чувствуете запахом: {data['smell']}\n"
        f"Как вы себя чувствуете?",
        reply_markup=feelings_keyboard
    )


# ----------------------
# Handle Feelings
# ----------------------
@router.callback_query(F.data == "feel_better")
async def handle_feel_better(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Рад, что вам стало лучше! 😊")

    data = await state.get_data()
    # Предлагаем продолжить
    await callback.message.answer("Вы можете подписаться на ежедневные напоминания для повторения этой техники.", reply_markup=give_subscribe_inline_keyboard(data.get("technique", "unknown")))
    await state.clear()


@router.callback_query(F.data == "feel_same")
async def handle_feel_same(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Понимаю, что вам пока не стало лучше. Давайте попробуем разобраться, что вас беспокоит. Напишите об этом или попробуйт другую технику.", reply_markup=main_menu_keyboard)

    await state.clear()
