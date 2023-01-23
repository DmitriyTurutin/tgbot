from aiogram import types
from handlers.states.SalesForm import SalesForm
from aiogram.utils.markdown import text


async def callback_sales_range(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        text="Ввод периода продаж\nНачало периода(*дд/мм/гггг*):", parse_mode="Markdown")

    await SalesForm.next()
