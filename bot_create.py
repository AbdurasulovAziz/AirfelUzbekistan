from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from languages import BOT_LANGUAGE
dotenv = dict(dotenv_values('.env'))

admin_chat = -1001630122577

storage = MemoryStorage()

LANGUAGE=BOT_LANGUAGE


bot = Bot(token=dotenv['BOT_TOKEN'])
dp = Dispatcher(bot, storage=storage)



