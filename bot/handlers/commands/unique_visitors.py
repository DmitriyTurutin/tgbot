from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.api_requests import get_prediction
from aiogram.utils.markdown import text


async def process_unique_visitors(message: types.Message, state: FSMContext):
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton(
            text="<< Вернуться обратно", callback_data="menu"
        )
        keyboard.add(btn_back)
        async with state.proxy() as data:
            data['unique_visitors'] = message.text
        # FIXME get unique visitors
        prediction = await get_prediction(int(message.text))
        prediction = round(prediction['prediction'], 2)
        await message.answer(text=f"Ваш прогноз на завтра: **{prediction} ₽**",
        reply_markup=keyboard,
        parse_mode="Markdown")
        await state.finish()