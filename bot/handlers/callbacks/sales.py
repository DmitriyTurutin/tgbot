from aiogram import types
from handlers.commands.sales import cmd_sales


async def callback_sales(callback_query: types.CallbackQuery):
    await cmd_sales(callback_query.message)
