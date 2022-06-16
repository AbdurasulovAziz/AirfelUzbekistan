
from bot_create import dp, bot, admin_id
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.db import MasterData
from keyboards import main_keyboard, sendAdmin_keyboard



class UserInfo(StatesGroup):
    sticker = State()
    photo=State()
    

class Photography(UserInfo):

    async def send_photo(message: types.Message):
        await bot.send_message(chat_id=message.from_user.id, text='Стикерни суратини жонатинг', reply_markup=types.ReplyKeyboardRemove())
        await UserInfo.sticker.set()

    @dp.message_handler(content_types='photo',state=UserInfo.sticker)
    async def __get_sticker(message: types.Message, state: FSMContext):
        await state.update_data(photo_sticker = message.photo[-1].file_id)
        await message.answer('Газ қозонни суратини жонатинг')
        await UserInfo.photo.set()
    
    @dp.message_handler(content_types='photo', state=UserInfo.photo)
    async def get_photo(message: types.Message, state:FSMContext):
        await state.update_data(photo = message.photo[-1].file_id)
        master_data = MasterData.get_master(message.from_user.id)
        data = await state.get_data()
        caption = f'Мастер: {master_data[1]}\nМастер рақами: {master_data[2]}'
        for chat_id in admin_id:
            await bot.send_photo(chat_id, data['photo_sticker'], caption=caption)
            await bot.send_photo(chat_id, data['photo'], caption=caption, reply_markup=sendAdmin_keyboard(message.from_user.id))
        await main_keyboard(message)
        
        @dp.callback_query_handler(regexp='(.+)-(.+)')
        async def accept(call: types.CallbackQuery, state:FSMContext):
            data = await state.get_data()
            callback = call.data.split('-')
            if callback[0] == 'Accept':
                MasterData.update_master_point(callback[1])
                await bot.send_message(chat_id=callback[1], text='Сизнинг аризангиз қабул қилинди')
                for chat_id in admin_id:
                    await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            elif callback[0] == 'Decline':
                await bot.send_message(chat_id=callback[1], text='Сизнинг аризангиз рад этилди')
                for chat_id in admin_id:
                    await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            await call.answer()
        await state.finish()
            
        
        
            
            
            
            