from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/mood")],
        [KeyboardButton(text="/relax")],
        [KeyboardButton(text="/support")],
        [KeyboardButton(text="/self_help")],
        [KeyboardButton(text="/feedback")],
    ],
    resize_keyboard=True,
)