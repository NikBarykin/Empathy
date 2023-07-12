from personal.relationship_goal import get_kb
from user_state import UserState

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def prepare(message: Message, state: FSMContext):
    await message.answer("Твой город")
    await state.set_state(UserState.city)


# TODO: allow mistakes and add more cities
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.lower())

    await message.answer(
            "Твоя цель",
            reply_markup=get_kb()
            )
    await state.set_state(UserState.relationship_goal)


async def process_invalid_city(message: Message):
    await message.reply("Я не знаю такого города")
