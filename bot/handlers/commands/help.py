from aiogram import types
from aiogram.utils.markdown import text


async def cmd_help(message: types.Message):
    await message.answer(
        text("""**🤖 Бот для hookah.work **
*Выполнили:* Васильев Даниил и Турутин Дмитрий
*Группа:* ФН11-33Б
*Версия:* 0.1 (alpha)
*Доступные функции:*
  - получение данных с сайта hooakh.work 
  - обновление данных
  - график посещаемости в виде bar plot
  - конвертация списка продаж в excel
*Доступные команды:* /credentials, /sales, /help /start"""),
        parse_mode="Markdown"
    )
