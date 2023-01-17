from aiogram import Dispatcher, Bot
from aiogram import types
from utils.api_requests import *


class CallbackHandlers:
    # Define "dp" as a class variable
    dp: Dispatcher
    bot = None
    url = None
    email = None
    password = None

    def __init__(self, _dp: Dispatcher, _bot: Bot) -> None:
        # Initialize "dp" with the passed in Dispatcher object
        self.dp = _dp
        self.bot = _bot

    # Continue callback
    @dp.callback_query_handler(lambda c: c.data == "continue")
    async def callback_continue(self, callback_query: types.CallbackQuery):
        # Create the inline keyboard with the "Go back << and "Get Sales Data buttons""
        global dp
        keyboard = types.InlineKeyboardMarkup()
        btn_sales = types.InlineKeyboardButton(
            text="Получить данные о продажах", callback_data="sales")
        btn_back = types.InlineKeyboardMarkup(
            text="Вернуться назад", callback_data="back")
        keyboard.add(btn_sales, btn_back)

        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Теперь выберете следующую команду",
            reply_markup=keyboard
        )

    # Go back callback
    @dp.callback_query_handler(lambda c: c.data == "back")
    async def callback_back(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Выберете следующую команду",
            reply_markup=None
        )
        # Go back to the previous command
        # await cmd_credentials(callback_query.message)

    # Update callback
    @dp.callback_query_handler(lambda c: c.data == "update")
    async def callback_update_sales(self, callback_query: types.CallbackQuery):
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton(
            text="Вернуться обратно", callback_data="sales"
        )

        keyboard.add(btn_back)
        await update_data(self.url, self.email, self.password)

        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Данные успешно обновлены!",
            reply_markup=keyboard
        )

    # Excel callback
    @dp.callback_query_handler(lambda c: c.data == "to_excel")
    async def callback_excel(self, callback_query: types.CallbackQuery):
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton(
            text="« Вернуться обратно", callback_data="sales_last_month"
        )

        keyboard.add(btn_back)

        file = get_excel()
        await self.bot.send_message(callback_query.message.chat.id, "Ваш файл:")
        await self.bot.send_document(callback_query.message.chat.id, document=file)
