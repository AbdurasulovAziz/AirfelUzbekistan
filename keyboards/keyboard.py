
from aiogram import types
from bot_create import admin_id





def get_phone_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(types.KeyboardButton('Контакт юборинг', request_contact=True))
    return keyboard


async def main_keyboard(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [types.KeyboardButton('Газ қозонни рўйхатдан ўтказиш'), types.KeyboardButton('Менинг анкетам👨🏻‍💼'), types.KeyboardButton('Бошқатдан рўйхатдан ўтиш🔄')]
    keyboard.add(*buttons)
    if message.from_user.id in admin_id:
        keyboard.add(types.KeyboardButton('Администратор бўлими'))
    await message.answer('Кейинги амални танланг:', reply_markup=keyboard)


def sendAdmin_keyboard(master_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text='Қабул қилиш',callback_data=f'Accept-{master_id}'), types.InlineKeyboardButton(text='Рад этиш', callback_data=f'Decline-{master_id}')]
    keyboard.add(*buttons)
    return keyboard


def get_data_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton('Маълумотларни юклаш'),types.KeyboardButton('Балларни айириш'),types.KeyboardButton('Ортга қайтиш⬅️')]
    keyboard.add(*buttons)
    return keyboard