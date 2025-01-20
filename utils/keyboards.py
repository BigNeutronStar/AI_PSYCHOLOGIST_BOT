from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/mood")],
        [KeyboardButton(text="/relax")],
        [KeyboardButton(text="/support")],
        [KeyboardButton(text="/self_help")],
        [KeyboardButton(text="/feedback")],
        [KeyboardButton(text="/help")],
        
    ],
    resize_keyboard=True,
)


relaxation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дыхательные упражнения", callback_data="breathing")],
    [InlineKeyboardButton(text="Медитация", callback_data="meditation")],
    [InlineKeyboardButton(text="Прогрессивная релаксация", callback_data="progressive")]
])




self_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дневник благодарности", callback_data="gratitude")],
    [InlineKeyboardButton(text="Упражнение 'Пять чувств'", callback_data="five_senses")],
])


def give_subscribe_inline_keyboard(technique: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", callback_data=f"subscribe_scheduler_{technique}")],
        [InlineKeyboardButton(text="Отписаться", callback_data=f"unsubscribe_scheduler_{technique}")],
        [InlineKeyboardButton(text="Отмена", callback_data=f"cancel_subscribe_scheduler")],
    ])

