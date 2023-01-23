from aiogram import types


async def callback_continue(callback_query: types.CallbackQuery):
    # Create the inline keyboard with the "go back << and "get sales data buttons""
    keyboard = types.InlineKeyboardMarkup()
    btn_sales = types.InlineKeyboardButton(
        text="Меню бота", callback_data="menu")
    btn_back = types.InlineKeyboardMarkup(
        text="<< Вернуться назад", callback_data="fix_credentials")
    keyboard.add(btn_back, btn_sales)

    await callback_query.message.edit_text(
        text="Теперь выберете следующую команду",
        reply_markup=keyboard
    )
