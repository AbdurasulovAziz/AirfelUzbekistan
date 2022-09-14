
from bot_create import dp, bot, LANGUAGE, admin_chat
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.db import MasterData
from keyboards import main_keyboard, sendAdmin_keyboard
import yadisk
import os
from datetime import datetime, timedelta


class UserInfo(StatesGroup):
    sticker = State()
    photo = State()


class Photography(UserInfo):

    async def send_photo(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await bot.send_message(chat_id=message.from_user.id, text=LANGUAGE[data['lang']]['SendSticker'],
                               reply_markup=types.ReplyKeyboardRemove())
        await UserInfo.sticker.set()

    @dp.message_handler(content_types='photo', state=UserInfo.sticker)
    async def __get_sticker(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await state.update_data(photo_sticker=message.photo[-1])
        await message.photo[-1].download(f'registration/yadiskIMG/{message.photo[-1].file_unique_id}.png')
        await message.answer(LANGUAGE[data['lang']]['PhotoKot'])
        await UserInfo.photo.set()

    @dp.message_handler(content_types='photo', state=UserInfo.photo)
    async def get_photo(message: types.Message, state: FSMContext):
        master_data = MasterData.get_master(message.from_user.id)
        data = await state.get_data()
        await message.photo[-1].download(f'registration/yadiskIMG/{message.photo[-1].file_unique_id}.png')
        caption = f'''{LANGUAGE[data['lang']]['Master']} {master_data[1]}\n{LANGUAGE[data['lang']]['MasterPhone']} {master_data[2]}'''
        await bot.send_photo(admin_chat, data['photo_sticker'].file_id, caption=caption)
        await bot.send_photo(admin_chat, message.photo[-1].file_id, caption=caption,
                             reply_markup=await sendAdmin_keyboard(message.from_user.id,data["lang"],
                                                                   data['photo_sticker'].file_unique_id))
        await state.reset_state(with_data=False)
        await main_keyboard(message, state)


    @dp.callback_query_handler(regexp='(.+)/(.+)/(.+)/(.+)')
    async def accept(call: types.CallbackQuery):
        y = yadisk.YaDisk(token='y0_AgAAAABkRiIFAAhhOQAAAADNxaUa5HggKsNbTYSdpfFYiKjje1KR5O4')
        callback = call.data.split('/')
        master_info = MasterData.get_master(callback[1])
        caption = f'''{LANGUAGE['У́збекча']['Master']} {master_info[1]}\n{LANGUAGE['У́збекча']['MasterPhone']} {master_info[2]}'''
        if callback[0] == 'Accept':
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Accepted"]}')

            filename = f'1. {(datetime.now() + timedelta(hours=3)).strftime("%Y_%m_%d %H_%M_%S")} {master_info[2]}'
            filename2 = f'2. {(datetime.now() + timedelta(hours=3)).strftime("%Y_%m_%d %H_%M_%S")} {master_info[2]}'

            with open(f'registration/yadiskIMG/{callback[3]}.png', 'rb') as imgfile:
                y.upload(imgfile, f'/AirfelUzbekistan/{filename}')

            with open(f'registration/yadiskIMG/{call.message.photo[-1].file_unique_id}.png', 'rb') as imgfile:
                y.upload(imgfile, f'/AirfelUzbekistan/{filename2}')

            os.remove(f'registration/yadiskIMG/{call.message.photo[-1].file_unique_id}.png')
            os.remove(f'registration/yadiskIMG/{callback[3]}.png')
            MasterData.update_master_point(callback[1])

            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourAccepted'])
        elif callback[0] == 'Decline':
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Declined"]}')
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourDecline'])
            os.remove(f'registration/yadiskIMG/{call.message.photo[-1].file_unique_id}.png')
            os.remove(f'registration/yadiskIMG/{callback[3]}.png')

        await call.answer()









