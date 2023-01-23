
from aiogram import types
from utils.api_requests import get_excel


async def callback_to_excel(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        text="<< Вернуться назад", callback_data="sales_data"
    )
    keyboard.add(btn_back)


    await callback_query.message.answer("Ваши данные в формате excel: ", reply_markup=keyboard)
    await callback_query.message.answer_document(document=await get_excel())