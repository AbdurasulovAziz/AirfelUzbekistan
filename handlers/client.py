from aiogram import Dispatcher, types
from bot_create import dp
from registration import Registration, Photography, TakePoints
from keyboards import main_keyboard, get_data_keyboard
from database import MasterData, AdminData
import pandas as pd


@dp.message_handler(commands='start')
async def start(message: types.Message):
    try:
        master_id = MasterData.get_master(message.from_user.id)
        if master_id == None:
            await message.answer('Аввал рўйхатдан ўтишингиз керак')
            await Registration.registration(message)
        else:
            await message.answer('Қуйидагилардан бирини танланг?')
            await main_keyboard(message)
    except TypeError:
        await message.answer('Бот уже запущен')
        await main_keyboard(message)

@dp.message_handler(lambda message: message.text == 'Менинг анкетам👨🏻‍💼')
async def get_info(message: types.Message):
        master = MasterData.get_master(message.from_user.id)
        text = f'''Сертификат рақами:{master[4]}\nИсм: {master[1]}\nРақам: {master[2]}\nБаллар: {master[3]}'''
        await message.answer(text)

@dp.message_handler(lambda message: message.text == 'Бошқатдан рўйхатдан ўтиш🔄')
async def update_info(message: types.Message):
    await Registration.registration(message)

@dp.message_handler(lambda message: message.text == 'Газ қозонни рўйхатдан ўтказиш')
async def send_photo(message: types.Message):
    await Photography.send_photo(message)

@dp.message_handler(lambda message: message.text == 'Администратор бўлими')
async def get_data(message: types.Message):
    await message.answer('Администратор панели:', reply_markup=get_data_keyboard())
    
    @dp.message_handler(lambda message: message.text == 'Маълумотларни юклаш')
    async def get_excel(message: types.Message):
        data = AdminData.get_master_data()
        columns = ['ID', 'Name', 'Number', 'Points', 'Certificate']
        array = []
        for i in data:
            arr = []
            for j in i:
                arr.append(str(j))
            array.append(arr)
        array = pd.DataFrame(array, columns=columns)
        array.to_excel('database/Маълумотлар.xlsx', index=False)
        await message.reply_document(open('database/Маълумотлар.xlsx', 'rb'))


    @dp.message_handler(lambda message: message.text == 'Балларни айириш')
    async def minusPoint(message: types.Message):
        await TakePoints.takePoints_state(message)

    @dp.message_handler(lambda message: message.text == 'Ортга қайтиш⬅️')
    async def get_back(message: types.Message):
        await main_keyboard(message)

    



        








def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')