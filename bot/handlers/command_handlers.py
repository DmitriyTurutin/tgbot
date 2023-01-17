from aiogram.utils.markdown import text
from aiogram import Bot, Dispatcher
from aiogram import types

class CommandHandlers:
    dp = None

    def __init__(self, _dp: Dispatcher) -> None:
        self.dp = _dp

    @dp.message_handler(commands='start')
    async def cmd_start(self, message: types.message):
        await message.answer(
            text("привет! этот бот создан для получения данных с сайта hookah crm\n\n *доступные команды:*\n",
                "/credentials — введите данные для входа в hookah.work\n",
                "/help — справка *(информация о боте)*"),
            reply=False,
            parse_mode="markdown")