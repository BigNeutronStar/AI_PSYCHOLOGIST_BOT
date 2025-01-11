from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Определить настроение")],
        [KeyboardButton(text="Рекомендации по релаксации")],
        [KeyboardButton(text="Психологическая поддержка")],
        [KeyboardButton(text="Техники самопомощи")],
        [KeyboardButton(text="Финальная анкета")],
    ],
    resize_keyboard=True,
)