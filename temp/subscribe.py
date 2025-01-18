from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.keyboards import main_menu_keyboard
from utils.scheduler import subscribe_daily_reminder, unsubscribe_daily_reminder
from config import bot

router = Router()

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
    return


@router.callback_query(F.data.startswith("unsubscribe_scheduler"))
async def unsubscribe_gratitude(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    technique_name = subscribe_techniques.get("_".join(callback.data.split('_')[2:]))

    unsubscribe_daily_reminder(chat_id, technique_name)
    await callback.message.answer(f"Вы отписались от ежедневных напоминаний для техники '{technique_name}'.",
                                  reply_markup=main_menu_keyboard)
    return


@router.callback_query(F.data == "cancel_subscribe_scheduler")
async def unsubscribe_gratitude(callback: CallbackQuery):
    await callback.message.answer("🫡", reply_markup=main_menu_keyboard)
    return
