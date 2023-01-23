from aiogram import types
from handlers.states.PredictForm import PredictForm


async def callback_predict(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Сколько гостей расчитываете принять?")
    await PredictForm.unique_visitors.set()




