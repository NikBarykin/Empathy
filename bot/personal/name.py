from user_state import UserState

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def process_name(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(name=message.text)

    # age
    await message.answer("Сколько тебе лет?")
    await state.set_state(UserState.age)

