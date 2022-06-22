from aiogram import Dispatcher, types
import aiogram
from bot_create import dp, LANGUAGE
from registration import Registration, Photography, TakePoints, choose_language
from keyboards import main_keyboard, get_data_keyboard, language_keyboard
from database import MasterData, AdminData
from aiogram.dispatcher import FSMContext
import pandas as pd


@dp.message_handler(commands='start')
async def start(message: types.Message, state:FSMContext):
    try:
        data = await state.get_data()
        master_id = MasterData.get_master(message.from_user.id)
        if master_id == None:
            await Registration.registration(message)
        else:
            try:
                await message.answer(LANGUAGE[data['lang']]['SelectNextDo'])
                await main_keyboard(message, state)
            except KeyError:
                await Registration.registration(message)
    except TypeError:
        await message.answer('Бот уже запущен')
        await main_keyboard(message, state)

@dp.message_handler(lambda message: message.text == 'Менинг анкетам👨🏻‍💼' or message.text == 'Моя анкета👨🏻‍💼')
async def get_info(message: types.Message, state:FSMContext):
    data = await state.get_data()
    master = MasterData.get_master(message.from_user.id)
    text = f'''{LANGUAGE[data['lang']]['Name']} {master[1]}\n{LANGUAGE[data['lang']]['Phone']} {master[2]}\n{LANGUAGE[data['lang']]['Points']} {master[3]}'''
    await message.answer(text)

@dp.message_handler(lambda message: message.text == 'Бошқатдан рўйхатдан ўтиш🔄' or message.text == 'Зарегистрироваться заново🔄')
async def update_info(message: types.Message):
    await Registration.registration(message)

@dp.message_handler(lambda message: message.text == 'Газ қозонни рўйхатдан ўтказиш' or message.text == 'Зарегистрировать котёл')
async def send_photo(message: types.Message, state:FSMContext):
    await Photography.send_photo(message, state)

@dp.message_handler(lambda message: message.text == 'Администратор бўлими' or message.text == 'Админ панель')
async def get_data(message: types.Message, state:FSMContext):
    data = await state.get_data()
    await message.answer(LANGUAGE[data['lang']]['AdminPanel'], reply_markup=await get_data_keyboard(state))
    
    @dp.message_handler(lambda message: message.text == 'Маълумотларни юклаш' or message.text == 'Получить данные')
    async def get_excel(message: types.Message):
        data = AdminData.get_excel()
        columns = ['Name', 'Phone', 'Points']
        array = []
        for i in data:
            arr = []
            for j in i:
                arr.append(str(j))
            array.append(arr)
        array = pd.DataFrame(array, columns=columns)
        array.to_excel('database/Маълумотлар.xlsx', index=False)
        await message.reply_document(open('database/Маълумотлар.xlsx', 'rb'))


    @dp.message_handler(lambda message: message.text == 'Балларни айириш' or message.text == 'Отнять баллы')
    async def minusPoint(message: types.Message, state:FSMContext):
        await TakePoints.takePoints_state(message, state)

    @dp.message_handler(lambda message: message.text == 'Ортга қайтиш⬅️' or message.text == 'Назад⬅️')
    async def get_back(message: types.Message, state:FSMContext):
        await main_keyboard(message, state)

    

@dp.message_handler(lambda message: message.text == 'Поменять язык' or message.text == 'Тилни у́згартириш')
async def change_lang(message: types.Message):
    await choose_language(message)
    
    
    






    

        








def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')