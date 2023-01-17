from aiogram import types
from utils.api_requests import fetch_sales_today, get_plot


async def callback_sales_today(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_excel = types.InlineKeyboardButton(
        text="В excel", callback_data="to_excel"
    )
    btn_back = types.InlineKeyboardButton(
        text="Вернуться обратно", callback_data="sales"
    )

    keyboard.add(btn_excel)
    keyboard.add(btn_back)

    data = fetch_sales_today()

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

        if len(data) == 0:
            reply_string = "Пусто!"
            btn_excel = None
        elif len(formatted_data) != 0:
            reply_string = "*Продажи за месяц:*\n" + \
                           '\n\n'.join(formatted_data)

        plot = get_plot()

    await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=plot, caption=reply_string,
                         reply_markup=keyboard, parse_mode="Markdown")
