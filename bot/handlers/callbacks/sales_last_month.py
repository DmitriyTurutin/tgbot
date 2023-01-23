from aiogram import types
from utils.api_requests import fetch_sales_last_month, get_barplot
from io import BytesIO
from utils.date_convertion import convert_date


async def callback_sales_last_month(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_excel = types.InlineKeyboardButton(
        text="В excel", callback_data="to_excel"
    )
    btn_back = types.InlineKeyboardButton(
        text="<< Вернуться назад", callback_data="menu"
    )

    keyboard.add(btn_back)
    keyboard.add(btn_excel)

    data = await fetch_sales_last_month()
    formatted_data = []

    for item in data:
        name = item[0]
        price = item[1]
        quantity = item[2]
        payment_method = item[3]
        customer = item[4]
        date = convert_date(item[5])

        formatted_item = f"*Товар:* {name},\n*Цена:* {price},\n*Кол-во:* {quantity},\n*Метод оплаты:* {payment_method},\n*Клиент:* {customer},\n*Дата:* {date}"
        if len(formatted_data) < 6:
            formatted_data.append(formatted_item)

        formatted_data.reverse()
        if len(formatted_data) != 0:
            reply_string = "*Продажи за месяц:*\n" + \
                           '\n\n'.join(formatted_data)
        else:
            reply_string = "Пусто!"
            btn_excel = None

    await callback_query.message.answer_photo(photo=await get_barplot(), caption=reply_string,
                                        reply_markup=keyboard, parse_mode="Markdown")
