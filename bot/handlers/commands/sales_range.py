from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.states.SalesForm import SalesForm
from utils.api_requests import fetch_sales_range
import requests
from main import bot
from io import BytesIO
from utils.regular_expression import check_re


async def process_from_date(message: types.Message, state: FSMContext):
    match = check_re(message.text)

    if match:
        await message.answer("Конец периода:")
        async with state.proxy() as data:
            data['from_date'] = message.text
        await SalesForm.next()
    else:
        await message.answer("Неправильный формат даты!")
        await state.finish()


async def process_to_date(message: types.Message, state: FSMContext):
    match = check_re(message.text)
    if not match:
        await message.answer("Неправльный формат даты!")
        await state.finish()
    else:
        async with state.proxy() as data:
            data['to_date'] = message.text
        keyboard = types.InlineKeyboardMarkup()
        btn_excel = types.InlineKeyboardButton(
            text="В excel", callback_data="to_excel"
        )

        from_date = data.get('from_date')
        to_date = data.get('to_date')

        keyboard.add(btn_excel)

        data = fetch_sales_range(from_date, to_date)
        formatted_data = []
        reply_string = ""

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

            if len(formatted_data) != 0:
                reply_string = "*Продажи за выбранный период:*\n" + \
                               '\n\n'.join(formatted_data)
            else:
                reply_string = "Пусто!"
                btn_excel = None

        response = requests.get("http://localhost:8000/download/sales.png")

        photo = BytesIO(response.content)
        photo.name = 'sales_last_month.xlsx'

        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=reply_string, reply_markup=keyboard,
                             parse_mode="Markdown")
        await state.finish()
