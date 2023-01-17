from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text
import requests
import re
from datetime import datetime
from io import BytesIO

import logging

logging.basicConfig(level=logging.INFO)

url =""
email = ""
password = ""

# Define a state for the bot

TOKEN = '5612271701:AAG1wFM9vnGRBvGnHMXxctaPECVNHBU2cWM'
local_URL = "http://localhost:8000"

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)



class CredentialsForm(StatesGroup):
    url = State()
    email = State()
    password = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer(
        text("Привет! Этот бот создан для получения данных с сайта hookah crm\n\n *Доступные команды:*\n",
             "/credentials — введите данные для входа в hookah.work\n",
             "/help — справка *(информация о боте)*"),
        reply=False,
        parse_mode="Markdown")


@dp.message_handler(commands='credentials')
async def cmd_credentials(message: types.Message):
    await CredentialsForm.url.set()
    await bot.send_message(message.from_user.id, "Введите url для hookah.work")


@dp.message_handler(state=CredentialsForm.url)
async def process_url(message: types.Message, state: FSMContext):

    await CredentialsForm.next()
    await message.answer("Введите email для hookah.work")
    async with state.proxy() as data:
        url = message.text.strip()
        data['url'] = message.text


@dp.message_handler(state=CredentialsForm.email)
async def process_email(message: types.Message, state: FSMContext):

    await CredentialsForm.next()
    await message.answer("Введите пароль для hookah.work")
    async with state.proxy() as data:
        data['email'] = message.text
        global email
        email = message.text.strip()


@dp.message_handler(state=CredentialsForm.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    
    global email
    global password
    global url
    url = data.get('url')
    email = data.get('email')
    password = data.get('password')

    await message.answer(
        text(f"**Ваш email:** {email}\n**Ваш пароль:** {password}"),
        reply=False,
        parse_mode="Markdown"
    )
    keyboard = types.InlineKeyboardMarkup()
    btn_continue = types.InlineKeyboardButton(
        text="Продолжить", callback_data="continue")
    btn_fix = types.InlineKeyboardButton(
        text="Исправить данные", callback_data="fix")
    keyboard.add(btn_continue, btn_fix)
    await message.answer("Теперь выберите одну из команд", reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "continue")
async def callback_continue(callback_query: types.CallbackQuery):
    # Create the inline keyboard with the "Go back << and "Get Sales Data buttons""
    keyboard = types.InlineKeyboardMarkup()
    btn_sales = types.InlineKeyboardButton(
        text="Получить данные о продажах", callback_data="sales")
    btn_back = types.InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="back")
    keyboard.add(btn_sales, btn_back)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Теперь выберете следующую команду",
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "back")
async def callback_back(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберете следующую команду",
        reply_markup=None
    )
    # Go back to the previous command
    await cmd_credentials(callback_query.message)


@dp.message_handler(commands="sales")
async def cmd_sales(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn_sales = types.InlineKeyboardButton(
        text="Получить данные о продажах", callback_data="sales")
    btn_back = types.InlineKeyboardMarkup(
        text="<-- вернуться назад")
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
        text="← вернутся назад ", callback_data="continue"
    )
    keyboard.add(btn_sales_today)
    keyboard.add(btn_sales_last_month)
    keyboard.add(btn_sales_range)
    keyboard.add(btn_back, btn_update)

    await bot.send_message(
        chat_id=message.chat.id,
        text="Меню данных о продажах",
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "sales")
async def callback_sales(callback_query: types.CallbackQuery):
    await cmd_sales(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == "update")
async def callback_update_sales(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        text="Вернуться обратно", callback_data="sales"
    )

    keyboard.add(btn_back)
    await update_data(url, email, password)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Данные успешно обновлены!",
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "sales_today")
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

    response = requests.get("http://localhost:8000/download/sales.png")

    photo = BytesIO(response.content)
    photo.name = 'sales_last_month.xlsx'

    await bot.send_photo(chat_id=callback_query.message.chat.id, photo=photo, caption=reply_string, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == "sales_last_month")
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

    await bot.send_photo(chat_id=callback_query.message.chat.id, photo=photo, caption=reply_string, reply_markup=keyboard, parse_mode="Markdown")


class SalesForm(StatesGroup):
    from_date = State()
    to_date = State()


@dp.callback_query_handler(lambda c: c.data == "sales_range")
async def callback_sales_range(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.message.chat.id, "Ввод периода продаж\n\n\nНачало периода(*дд/мм/гг*):", parse_mode="Markdown")

    await SalesForm.next()


@dp.message_handler(state=SalesForm.from_date)
async def process_from_date(message: types.Message, state: FSMContext):
    match = await check_re(message.text)

    if match:
        await message.answer("Конец периода:")
        async with state.proxy() as data:
            data['from_date'] = message.text
        await SalesForm.next()
    else:
        await message.answer("Неправильный формат даты!")
        await state.finish()


@dp.message_handler(state=SalesForm.to_date)
async def process_to_date(message: types.Message, state: FSMContext):
    match = await check_re(message.text)
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

        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=reply_string, reply_markup=keyboard, parse_mode="Markdown")
        await state.finish()


async def check_re(string: str) -> bool:
    match = re.match(r"\d{2}/\d{2}/\d{4}", string.strip())
    return match


@dp.callback_query_handler(lambda c: c.data == "to_excel")
async def callback_excel(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        text="« Вернуться обратно", callback_data="sales_last_month"
    )

    keyboard.add(btn_back)

    response = requests.get("http://localhost:8000/download/sales.xlsx")

    file = BytesIO(response.content)
    file.name = 'sales.xlsx'

    await bot.send_message(callback_query.message.chat.id, "Ваш файл:")
    await bot.send_document(callback_query.message.chat.id, document=file)


async def update_data(url, email, password):
    url = 'http://localhost:8000/update'
    email = 'aleksandrdonskov@gmail.com'
    password = 'hpkorolev2020'
    headers = {'Content-Type': 'application/json'}
    data = {'url': url, 'email': email, 'password': password}

    response = requests.get(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())


def fetch_sales_today():
    url = 'http://localhost:8000/sales/today'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    print(response.status_code)
    return response.json()


def fetch_sales_last_month():
    url = 'http://localhost:8000/sales/last_month'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    print(response.status_code)
    return response.json()


def fetch_sales_range(from_date: str, to_date: str):
    url = 'http://localhost:8000/sales'
    headers = {'Content-Type': 'application/json'}

    # parse the string date to datetime object
    from_date = datetime.strptime(from_date, '%d/%m/%Y')
    to_date = datetime.strptime(to_date, '%d/%m/%Y')
    data = {'from_date': from_date.isoformat(), 'to_date': to_date.isoformat()}

    try:
        response = requests.get(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        logging.error("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Something went wrong", err)


def fetch_sales_data(email, password):
    # TODO: implement this function
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
