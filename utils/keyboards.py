from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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


def give_subscribe_inline_keyboard(technique: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", callback_data=f"subscribe_scheduler_{technique}")],
        [InlineKeyboardButton(text="Отписаться", callback_data=f"unsubscribe_scheduler_{technique}")],
        [InlineKeyboardButton(text="Отмена", callback_data=f"cancel_subscribe_scheduler")],
    ])
