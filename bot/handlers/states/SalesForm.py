from aiogram.dispatcher.filters.state import StatesGroup, State


class SalesForm(StatesGroup):
    from_date = State()
    to_date = State()
