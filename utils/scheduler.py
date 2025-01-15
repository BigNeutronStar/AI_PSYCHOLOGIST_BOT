from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

# Инициализация планировщика
scheduler = AsyncIOScheduler()


# Функция для отправки напоминания
async def send_daily_reminder(bot: Bot, chat_id: int, technique_name: str):
    message = f"Напоминание: пора выполнить технику '{technique_name}'."
    await bot.send_message(chat_id=chat_id, text=message)


# Функция для подписки на ежедневные напоминания
def subscribe_daily_reminder(bot: Bot, chat_id: int, technique_name: str):
    job_id = f"daily_reminder_{chat_id}_{technique_name}"
    scheduler.add_job(
        send_daily_reminder,
        trigger=CronTrigger(hour=10),  # Ежедневно в 10 утра
        kwargs={"bot": bot, "chat_id": chat_id, "technique_name": technique_name},
        id=job_id,
        replace_existing=True  # Заменяет задачу, если она уже существует
    )


# Функция для отписки от ежедневных напоминаний
def unsubscribe_daily_reminder(chat_id: int, technique_name: str):
    job_id = f"daily_reminder_{chat_id}_{technique_name}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)


# Запуск планировщика
def start_scheduler():
    scheduler.start()
