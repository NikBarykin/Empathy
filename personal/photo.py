from user_state import UserState

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def process_photo(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(photo=message.photo[0].file_id)
    await message.reply("Отлично выглядите!")

    # self-description
    # TODO: why 240?
    await message.answer("Напиши немного о себе в свободной форме (не более 240 символов)")
    await state.set_state(UserState.self_description)
