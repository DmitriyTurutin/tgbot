import aiogram
import requests

from aiogram.utils import executro 
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

TOKEN = ''
URL = ''

bot = aiogram.Bot(TOKEN)

async def on_startup(dp):
    await bot.set_webhook(URL)


# Create command handlers
async def sales_last_month(message: Message):
    r = request.get(URL)
