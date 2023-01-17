from aiogram import types

from utils.api_requests import update_data
from entities.Credentials import Credentials


async def callback_update_sales(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        text="Вернуться обратно", callback_data="sales"
    )

    keyboard.add(btn_back)

    credentials = Credentials()

    # await update_data(credentials.url, credentials.email, credentials.password)

    await callback_query.message.edit_text(
        text="Данные успешно обновлены!",
        reply_markup=keyboard
    )
