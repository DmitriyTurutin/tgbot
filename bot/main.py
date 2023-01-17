import logging

from aiogram import Bot, Dispatcher, executor
from config import Config

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Initialize bot
storage = MemoryStorage()
TOKEN = '5612271701:AAG1wFM9vnGRBvGnHMXxctaPECVNHBU2cWM'
bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=storage)

# Register all handlers


if __name__ == '__main__':
    executor.start_polling(dp)


