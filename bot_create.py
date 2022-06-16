from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

dotenv = dict(dotenv_values('.env'))

storage = MemoryStorage()


bot = Bot(token=dotenv['BOT_TOKEN'])
dp = Dispatcher(bot, storage=storage)


admin_id = [int(x) for x in dotenv['ADMIN_ID'].split(',')]

