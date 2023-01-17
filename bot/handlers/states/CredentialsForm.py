from aiogram.dispatcher.filters.state import StatesGroup, State


class CredentialsForm(StatesGroup):
    url = State()
    email = State()
    password = State()
