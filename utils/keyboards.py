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


relaxation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дыхательные упражнения", callback_data="breathing")],
    [InlineKeyboardButton(text="Медитация", callback_data="meditation")],
    [InlineKeyboardButton(text="Прогрессивная релаксация", callback_data="progressive")]
])


self_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дневник благодарности", callback_data="gratitude")],
    [InlineKeyboardButton(text="Упражнение 'Пять чувств'", callback_data="five_senses")]
])


def give_subscribe_inline_keyboard(technique: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", callback_data=f"subscribe_scheduler_{technique}")],
        [InlineKeyboardButton(text="Отписаться", callback_data=f"unsubscribe_scheduler_{technique}")],
        [InlineKeyboardButton(text="Отмена", callback_data=f"cancel_subscribe_scheduler")],
    ])


def create_feedback_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="feedback:1"),
            InlineKeyboardButton(text="2", callback_data="feedback:2"),
            InlineKeyboardButton(text="3", callback_data="feedback:3"),
            InlineKeyboardButton(text="4", callback_data="feedback:4"),
            InlineKeyboardButton(text="5", callback_data="feedback:5"),
        ]
    ])
    return keyboard


