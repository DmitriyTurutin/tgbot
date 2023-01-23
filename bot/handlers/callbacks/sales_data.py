from aiogram import types


async def callback_sales_data(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_sales_today = types.InlineKeyboardButton(
        text="Данные за день", callback_data="sales_day"
    )
    btn_sales_month = types.InlineKeyboardButton(
        text="Данные за месяц", callback_data="sales_month"
    )
    btn_sales_range = types.InlineKeyboardButton(
        text="Выбрать период данных", callback_data="sales_range"
    )
    btn_back = types.InlineKeyboardButton(
        text="<< Вернуться назад", callback_data="menu"
    )
    keyboard.add(btn_sales_today, btn_sales_month)
    keyboard.add(btn_sales_range)
    keyboard.add(btn_back)

    await callback_query.message.edit_text(text="Меню данных по продажам", reply_markup=keyboard)