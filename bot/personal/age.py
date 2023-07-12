from user_state import UserState
from personal.sex import get_kb

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))

    await message.answer(
            "Твой пол?",
            reply_markup=get_kb())

    await state.set_state(UserState.sex)


async def process_invalid_age(message: Message):
    # TODO: more clear comment
    await message.reply("Некорректное значение")
