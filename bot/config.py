import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    TOKEN = os.environ.get('TOKEN')