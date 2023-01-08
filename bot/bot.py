from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceutor
from aiogram.utils.markdown import text, hlink

import logging

logging.basicConfig(level=logging.INFO)

TOKEN = '5612271701:AAG1wFM9vnGRBvGnHMXxctaPECVNHBU2cWM'
URL = 'https://9850-79-139-245-121.ngrok.io'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

credentials = {}

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply(
        text("Привет! Этот бот создан для получения данных с сайта hookah crm\n\n *Доступные команды:*\n",
             hlink("/credentials", "Введите данные для входа в hookah.work"),
             hlink("/help", "справка *(информация о боте)*")),
        reply=False,
        parse_mod="Markdown")


@dp.message_handler(commands='credentials')
async def cmd_credentials(message: types.Message):
    email = ""
    password = ""

    await message.reply("Ввести email для hookah.work")
    response = await bot.wait_for_message(chat_id=message.chat.id)

    email = response.text

    await message.reply("Введите пароль для hookah.work")

    response = await bot.wait_for_message(chat_id=message.chat.id)

    password = response.text

    credentials[message.chat.id] = (email, password)

    await message.reply(
        text("Your credentials: ",
             hlink(email, email),
             text(", "),
             hlink(password, password)),
        reply=False,
        parse_mode="Markdown"
    )

    # Create the inline keyboard with the "Продолжить"(continue) and "Исправить данные" (fix credentials) buttons
    keyboard = types.InlineKeyboardMarkup()
    btn_continue = types.InlineKeyboardButton(
        text="Продолжить", callback_data="continue")
    btn_fix = types.InlineKeyboardButton(
        text="Исправить данные", callback_data="fix")
    keyboard.add(btn_continue, btn_fix)
    # Send the message with the inline keyboard
    await message.reply("Теперь выберите одну из команд", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "continue")
async def callback_continue(callback_query: types.CallbackQuery):
    # Create the inline keyboard with the "Go back << and "Get Sales Data buttons""
    keyboard = types.InlineKeyboardMarkup()
    btn_sales = types.InlineKeyboardButton(
        text="Получить данные о продажах", callback_data="sales")
    btn_back = types.InlineKeyboardMarkup(text="Вернуться назад ↲")
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


@dp.callback_query_handler(lambda c: c.data == "sales")
async def callback_sales(callback_query: types.CallbackQuery):
    email, password = credentials[callback_query.message.chat.id]
    # Fetch the sales data using the email and password provided by the user
    sales_data = fetch_sales_data(email, password)
    # Send the sales data to the user
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=sales_data)


def fetch_sales_data(email, password):
    # TODO: implement this function
    pass


if __name__ == '__main__':
    exceutor.start_polling(dp, skip_updates=True)
