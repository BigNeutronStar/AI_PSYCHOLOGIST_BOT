from aiogram.fsm.state import State, StatesGroup


class FeedbackStates(StatesGroup):
    waiting_for_question_1 = State()
    waiting_for_question_2 = State()
    waiting_for_question_3 = State()
    waiting_for_question_4 = State()
    waiting_for_question_5 = State()
