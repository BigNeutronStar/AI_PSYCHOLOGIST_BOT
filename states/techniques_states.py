from aiogram.fsm.state import StatesGroup, State


class GratitudeStates(StatesGroup):
    first = State()
    second = State()
    third = State()


class FiveSensesStates(StatesGroup):
    see = State()
    hear = State()
    feel = State()
    taste = State()
    smell = State()