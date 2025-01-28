from aiogram.fsm.state import State, StatesGroup


class GeneralStates(StatesGroup):
    waiting_for_support = State()
    waiting_for_mood = State()
