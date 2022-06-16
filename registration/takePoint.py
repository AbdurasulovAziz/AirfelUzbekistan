from bot_create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import MasterData
from keyboards.keyboard import main_keyboard


class MasterPoint(StatesGroup):

    master_id = State()
    points = State()


class TakePoints(MasterPoint):

    async def takePoints_state(message: types.Message):
        await message.answer('Мастер сертификатини киритинг', reply_markup=types.ReplyKeyboardRemove())
        await MasterPoint.master_id.set()

    @dp.message_handler(state=MasterPoint.master_id)
    async def __get_master_id(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(certificate = int(message.text))
            await message.answer('Қанча балл айириш кераклигини киритинг::')
            await MasterPoint.points.set()
        else:
            await message.answer('Рақамли қийматни киритинг')
            await MasterPoint.master_id.set()

    @dp.message_handler(state=MasterPoint.points)
    async def __get_points(message:types.Message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(points = int(message.text))
            data = await state.get_data()
            MasterData.minus_master_point(data['certificate'], data['points'])
            await message.answer('Мастер маълумотлари янгиланди')
            await main_keyboard(message)
            await state.finish()
        else:
            await message('Рақамли қийматни киритинг')
            await MasterPoint.points.set()
