from aiogram import types
from handlers.states.CredentialsForm import CredentialsForm
from aiogram.utils.markdown import text
from aiogram.dispatcher import FSMContext


async def cmd_credentials(message: types.Message):
    await message.answer("Введите url для hookah.work")
    await CredentialsForm.url.set()


async def process_url(message: types.Message, state: FSMContext):
    await CredentialsForm.next()
    await message.answer("Введите email для hookah.work")
    async with state.proxy() as data:
        url = message.text.strip()
        data['url'] = message.text


async def process_email(message: types.message, state: FSMContext):
    await CredentialsForm.next()
    await message.answer("Введите пароль для hookah.work")
    async with state.proxy() as data:
        data['email'] = message.text
        email = message.text.strip()


async def process_password(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    url = data['url'].strip()
    email = data['email'].strip()
    password = data['password'].strip()
    await message.answer(
        text(f"""**ваш url:** {url}
**ваш email:** {email}
**ваш пароль:** {password}"""),
        reply=False,
        parse_mode="markdown"
    )
    keyboard = types.InlineKeyboardMarkup()
    btn_continue = types.InlineKeyboardButton(
        text="продолжить", callback_data="continue")
    btn_fix = types.InlineKeyboardButton(
        text="исправить данные", callback_data="fix")
    keyboard.add(btn_continue, btn_fix)
    await message.answer("теперь выберите одну из команд", reply_markup=keyboard)
    await state.finish()
