
from pip import main
from bot_create import dp, LANGUAGE
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import MasterData
from keyboards import get_phone_keyboard, main_keyboard, language_keyboard



class MasterInfo(StatesGroup):
    language = State()
    username = State()
    phone = State()
    

class Registration(MasterInfo):


    async def registration(message: types.Message):
        await message.answer('Выберите язык:\nТилни танланг:', reply_markup=language_keyboard())
        await MasterInfo.language.set()

        @dp.message_handler(state=MasterInfo.language)
        async def __get_lang(message: types.Message, state:FSMContext):
            if message.text in ['Русский', 'У́збекча']:
                await state.update_data(lang=message.text)
                data = await state.get_data()
                if True:
                    await message.answer(LANGUAGE[data['lang']]['SendName'], reply_markup=types.ReplyKeyboardRemove())
                await MasterInfo.username.set()
            else:
                await message.answer('Выберите на клавиатуре')
                await MasterInfo.language.set()

        @dp.message_handler(state=MasterInfo.username)
        async def __get_username(message: types.Message, state: FSMContext):
            data = await state.get_data()
            if len(message.text.split()) == 2:
                await state.update_data(master_name = message.text)
                await message.answer(LANGUAGE[data['lang']]['SendPhone_keyboard'],
                                     reply_markup=await get_phone_keyboard(state))
                await MasterInfo.phone.set()
            else:
                await message.answer(LANGUAGE[data['lang']]['TryAgain'])
                await MasterInfo.username.set()

        @dp.message_handler(content_types='contact', state=MasterInfo.phone)
        async def __get_phone(message: types.Message, state: FSMContext):
            await state.update_data(master_phone=message['contact']['phone_number'],
                                    master_id=message['contact']['user_id'])
            master = MasterData.get_master(message.from_user.id)
            master_data = await state.get_data()
            if master == None:
                MasterData.add_master(master_data['master_id'], master_data['master_name'], master_data['master_phone'])
                await message.answer(LANGUAGE[master_data['lang']]['AccountCreated'],
                                     reply_markup=types.ReplyKeyboardRemove())
            else:
                MasterData.update_master(master_data['master_id'], master_data['master_name'],
                                         master_data['master_phone'])
                await message.answer(LANGUAGE[master_data['lang']]['AccountUpdated'],
                                     reply_markup=types.ReplyKeyboardRemove())
            await state.reset_state(with_data=False)
            await main_keyboard(message, state)      


class LanguageInfo(StatesGroup):
    
    language = State()


async def choose_language(message: types.Message):
    await message.answer('Выберите язык:\nТилни танланг:', reply_markup=language_keyboard())
    await LanguageInfo.language.set()

    @dp.message_handler(state=LanguageInfo.language)
    async def __leng(message: types.Message, state: FSMContext):

        if message.text in ['Русский', 'У́збекча']:
                await state.update_data(lang=message.text)
                await main_keyboard(message, state)
                await state.reset_state(with_data=False)
        else:
            await message.answer('Выберите на клавиатуре\nKlaviaturadan tanlang')
            await MasterInfo.language.set()
