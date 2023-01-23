from aiogram import types
from utils.api_requests import brief_update_data


async def callback_brief_scan(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        text="<< Вернуться назад", callback_data="update"
    ) 

    keyboard.add(btn_back)
    await callback_query.message.answer("Обновляю данные, приблизительное время ожидания: 5 секунд")
    await brief_update_data()
    await callback_query.message.answer("Данные успешно обновлены", reply_markup=keyboard)