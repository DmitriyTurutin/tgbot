from aiogram import types
from aiogram.utils.markdown import text


async def cmd_sales(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn_update_data = types.InlineKeyboardButton(
        text="Обновить данные", callback_data="update"
    )
    btn_sales_data = types.InlineKeyboardButton(
        text="Получить данные по продажам", callback_data="sales_data"
    )

    btn_predict = types.InlineKeyboardButton(
        text="Предсказать продажи на завтра", callback_data="predict"
    )

    btn_back = types.InlineKeyboardButton(
        text="<< Вернутся назад ", callback_data="continue"
    )
    keyboard.add(btn_predict)
    keyboard.add(btn_sales_data)
    keyboard.add(btn_update_data)
    keyboard.add(btn_back)

    await message.answer(
        text("Меню бота\n1. с помощью градиентного бустинга предсказать данные (для баз от 5000 строк продаж)\n2. получить данные по продажам\n3. обновить данные с сайта"),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
