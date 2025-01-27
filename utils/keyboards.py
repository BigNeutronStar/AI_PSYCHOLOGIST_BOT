from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu_buttons_texts = ("Определение настроения", "Релакс", "Поддержка", "Успокоить себя самостоятельно", "Фидбек",
                           "Горячие линии поддержки и помощь")

# Клавиатура главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Определение настроения")],
        [KeyboardButton(text="Релакс")],
        [KeyboardButton(text="Поддержка")],
        [KeyboardButton(text="Успокоить себя самостоятельно")],
        [KeyboardButton(text="Фидбек")],
        [KeyboardButton(text="Горячие линии поддержки и помощь")],
        
    ],
    resize_keyboard=True,
)


relaxation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дыхательные упражнения", callback_data="breathing")],
    [InlineKeyboardButton(text="Медитация", callback_data="meditation")],
    [InlineKeyboardButton(text="Прогрессивная релаксация", callback_data="progressive")]
])

feelings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Лучше", callback_data="feel_better")],
        [InlineKeyboardButton(text="Без изменений", callback_data="feel_same")]
    ])


self_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дневник благодарности", callback_data="gratitude")],
    [InlineKeyboardButton(text="Упражнение 'Пять чувств'", callback_data="five_senses")],
])


def give_start_technique_keyboard(technique: str):
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data=f"start_{technique}")],
            [InlineKeyboardButton(text="Управление подпиской на эту технику", callback_data=f"change_subscription_{technique}")]
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


