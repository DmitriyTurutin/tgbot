from aiogram.dispatcher.filters.state import StatesGroup, State


class PredictForm(StatesGroup):
    unique_visitors = State()

