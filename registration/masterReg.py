
from bot_create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import MasterData
from keyboards import get_phone_keyboard, main_keyboard



class MasterInfo(StatesGroup):
    username = State()
    certificate = State()
    phone = State()
    

class Registration(MasterInfo):


    async def registration(message: types.Message):
        await message.answer('Исм ва фамилиянгизни киритинг', reply_markup=types.ReplyKeyboardRemove())
        await MasterInfo.username.set()

        @dp.message_handler(state=MasterInfo.username)
        async def __get_username(message: types.Message, state: FSMContext):
            if len(message.text.split()) == 2:
                await state.update_data(master_name = message.text)
                await message.answer('Сертификат рақамингизни киритинг')
                await MasterInfo.certificate.set()
            else:
                await message.answer('Қайта уриниб кўринг')
                await MasterInfo.username.set()

        @dp.message_handler(state=MasterInfo.certificate)
        async def __get_certificate(message: types.Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(master_certificate = message.text)
                await message.answer('Рақамингизни юборинг',reply_markup=get_phone_keyboard())
                await MasterInfo.phone.set()
            else:
                await message.answer('Сиз нотўғри маълумотларни киритдингиз, қайта уриниб кўринг')
                await MasterInfo.certificate.set()

        @dp.message_handler(content_types='contact', state=MasterInfo.phone)
        async def __get_phone(message: types.Message, state: FSMContext):
            await state.update_data(master_phone = message['contact']['phone_number'], master_id = message['contact']['user_id'])
            master = MasterData.get_master(message.from_user.id)
            master_data = await state.get_data()
            if master == None:
                MasterData.add_master(master_data['master_id'], master_data['master_name'], master_data['master_phone'], master_data['master_certificate'])
                await message.answer('Рўйхатдан ўтдингиз', reply_markup=types.ReplyKeyboardRemove())
            else:
                MasterData.update_master(master_data['master_id'], master_data['master_name'], master_data['master_phone'], master_data['master_certificate'])
                await message.answer('Анкета янгиланди', reply_markup=types.ReplyKeyboardRemove())
            
            await state.finish()
            await main_keyboard(message)      

