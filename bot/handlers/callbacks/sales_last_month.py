from aiogram import types
from utils.api_requests import fetch_sales_last_month
from io import BytesIO
import requests


async def callback_sales_last_month(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_excel = types.InlineKeyboardButton(
        text="В excel", callback_data="to_excel"
    )

    keyboard.add(btn_excel)

    data = fetch_sales_last_month()
    formatted_data = []

    for item in data:
        name = item[0]
        price = item[1]
        quantity = item[2]
        payment_method = item[3]
        customer = item[4]
        date = item[5]

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

    response = requests.get("http://localhost:8000/download/sales.png")

    photo = BytesIO(response.content)
    photo.name = 'sales_last_month.xlsx'

    await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=photo, caption=reply_string,
                                        reply_markup=keyboard, parse_mode="Markdown")
