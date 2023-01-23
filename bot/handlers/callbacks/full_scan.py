from aiogram import types
import time
from entities.Credentials import Credentials
from utils.api_requests import scan_update_data


async def callback_full_scan(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        text="<< Вернуться назад", callback_data="update"
    )

    keyboard.add(btn_back)
    await callback_query.message.answer("Обновляю данные, приблизительное время ожидания: 3 минуты")
    await scan_update_data()
    await callback_query.message.answer("Данные успешно обновлены", reply_markup=keyboard)
