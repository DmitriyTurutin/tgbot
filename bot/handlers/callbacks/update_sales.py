from aiogram import types

from entities.Credentials import Credentials


async def callback_update_sales(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_full_scan = types.InlineKeyboardButton(
        text="Полное сканирование", callback_data="full_scan"
    )
    btn_brief_scan = types.InlineKeyboardButton(
        text="Обновить (max 100 новых)", callback_data="brief_scan"
    )
    btn_back = types.InlineKeyboardButton(
        text="<< Вернуться обратно", callback_data="menu"
    )

    keyboard.add(btn_brief_scan, btn_full_scan)
    keyboard.add(btn_back)


    # await update_data(credentials.url, credentials.email, credentials.password)

    await callback_query.message.edit_text(
        text="1. Обновить первые 100 записей\n2. Полное сканирывание всех данных",
        reply_markup=keyboard
    )
