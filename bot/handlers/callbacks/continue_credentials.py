from aiogram import types


async def callback_continue(callback_query: types.CallbackQuery):
    # Create the inline keyboard with the "go back << and "get sales data buttons""
    keyboard = types.InlineKeyboardMarkup()
    btn_sales = types.InlineKeyboardButton(
        text="Получить данные о продажах", callback_data="sales")
    btn_back = types.InlineKeyboardMarkup(
        text="<< Вернуться назад", callback_data="back")
    keyboard.add(btn_sales, btn_back)

    await callback_query.message.edit_text(
        text="Теперь выберете следующую команду",
        reply_markup=keyboard
    )
