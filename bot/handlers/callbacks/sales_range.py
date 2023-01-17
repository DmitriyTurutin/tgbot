from aiogram import types
from handlers.states.SalesForm import SalesForm


async def callback_sales_range(callback_query: types.CallbackQuery):
    await callback_query.message.answer(callback_query.message.chat.id,
                                        "Ввод периода продаж\n\n\nНачало периода(*дд/мм/гг*):", parse_mode="Markdown")

    await SalesForm.next()
