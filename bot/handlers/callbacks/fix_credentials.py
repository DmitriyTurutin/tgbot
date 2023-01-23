from aiogram import types
from handlers.commands.credentials import cmd_credentials


async def callback_fix_credentials(callback_query: types.CallbackQuery):
    await cmd_credentials(callback_query.message)