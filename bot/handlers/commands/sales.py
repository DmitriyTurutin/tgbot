from aiogram import types
from aiogram.utils.markdown import text


async def cmd_sales(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn_sales = types.InlineKeyboardButton(
        text="Получить данные о продажах", callback_data="sales")
    btn_back = types.InlineKeyboardMarkup(
        text="<< Вернуться назад")
    keyboard.add(btn_sales, btn_back)

    keyboard = types.InlineKeyboardMarkup()
    btn_update = types.InlineKeyboardButton(
        text="Обновить данные", callback_data="update"
    )
    btn_sales_today = types.InlineKeyboardButton(
        text="Получить данные по продажам за день", callback_data="sales_today"
    )
    btn_sales_last_month = types.InlineKeyboardButton(
        text="Получить данные по продажам за месяц", callback_data="sales_last_month"
    )
    btn_sales_range = types.InlineKeyboardButton(
        text="Выбрать период данных по продажам", callback_data="sales_range"
    )

    btn_back = types.InlineKeyboardButton(
        text="<< Вернутся назад ", callback_data="continue"
    )
    keyboard.add(btn_sales_today)
    keyboard.add(btn_sales_last_month)
    keyboard.add(btn_sales_range)
    keyboard.add(btn_back, btn_update)

    await message.answer(
        text("Меню данных о продажах"),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
