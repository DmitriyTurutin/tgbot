from aiogram import types
from aiogram.utils.markdown import text


async def cmd_start(message: types.message):
    await message.answer(
        text("привет! этот бот создан для получения данных с сайта hookah crm\n\n *доступные команды:*\n",
             "/credentials — введите данные для входа в hookah.work\n",
             "/help — справка *(информация о боте)*"),
        reply=False,
        parse_mode="markdown")
