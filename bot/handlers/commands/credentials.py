from aiogram import types
from handlers.states.CredentialsForm import CredentialsForm
from aiogram.utils.markdown import text
from aiogram.dispatcher import FSMContext
from utils.api_requests import get_user
from utils.date_convertion import convert_date




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


async def process_password(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    url = data['url'].strip()
    email = data['email'].strip()
    password = data['password'].strip()

    user = await get_user(url, email, password)

    if not user['last_updated']:
        user['last_updated'] = 'данные отсутствуют'

    await message.answer(
        text(f"""**ваш url:** {user['url']}
**ваш email:** {user['email']}
**ваш пароль:** {user['password']}
**последнее обновление:** {convert_date(user['last_updated'].split(".")[0])}"""),
        reply=False,
        parse_mode="markdown"
    )
    keyboard = types.InlineKeyboardMarkup()
    btn_continue = types.InlineKeyboardButton(
        text="Продолжить", callback_data="continue")
    btn_fix = types.InlineKeyboardButton(
        text="Исправить данные", callback_data="fix_credentials")
    keyboard.add(btn_continue, btn_fix)
    await message.answer("Теперь выберете одну из команд", reply_markup=keyboard)
    await state.finish()
