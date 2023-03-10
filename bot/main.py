import logging
import os
from aiogram import Bot, Dispatcher, executor
from config import Config
from register_handlers import register_handlers
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Initialize bot
storage = MemoryStorage()
TOKEN = os.environ['BOT_TOKEN']
bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=storage)

# Register all handlers
register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp)


