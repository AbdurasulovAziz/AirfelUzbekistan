from bot_create import dp, LANGUAGE
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import MasterData
from database.db import AdminData
from keyboards.keyboard import main_keyboard


class MasterPoint(StatesGroup):

    master_number = State()
    points = State()


class TakePoints(MasterPoint):

    async def takePoints_state(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await message.answer(LANGUAGE[data['lang']]['MasterNum'], reply_markup=types.ReplyKeyboardRemove())
        await MasterPoint.master_number.set()

    @dp.message_handler(state=MasterPoint.master_number)
    async def __get_master_id(message: types.Message, state: FSMContext):
        master = AdminData.get_master_data()
        master_phone = [i[2] for i in master]
        data = await state.get_data()
        if message.text in master_phone:
            await state.update_data(master_number = message.text)
            await message.answer(LANGUAGE[data['lang']]['MinusPoints'])
            await MasterPoint.points.set()
        else:
            await message.answer(LANGUAGE[data['lang']]['NoTel'])
            await MasterPoint.master_number.set()

    @dp.message_handler(state=MasterPoint.points)
    async def __get_points(message:types.Message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(points = int(message.text))
            data = await state.get_data()
            MasterData.minus_master_point(data['master_number'], data['points'])
            await message.answer(LANGUAGE[data['lang']]['MasterUpdated'])
            await main_keyboard(message, state)
            await state.reset_state(with_data=False)
        else:
            data = await state.get_data()
            await message.answer(LANGUAGE[data['lang']]['SendDig'])
            await MasterPoint.points.set()
