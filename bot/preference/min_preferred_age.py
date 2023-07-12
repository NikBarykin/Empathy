from user_state import UserState

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


# TODO: invalid value
async def process_min_preferred_age(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(min_preferred_age=int(message.text))

    # max-preferred-age
    await message.answer("Укажи максимальный возраст партнера")
    await state.set_state(UserState.max_preferred_age)
