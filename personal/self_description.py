from user_state import UserState

# 3rd party
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )


## TODO: move to other place
#async def insert_personal(
#        async_session: async_sessionmaker[AsyncSession],
#        personal: Personal,
#        ) -> None:
#    async with async_session() as session:
#        async with session.begin():
#            session.add(personal)


async def process_self_description(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(self_description=message.text)

    #data = await state.get_data()
    #await insert_personal(
    #        async_session,
    #        Personal.from_fsm_data(data),
    #        )

    # TODO: check if user already filled their preferences
    # minimal preferred age
    await message.answer("Укажите минимальный возраст партнера")
    await state.set_state(UserState.min_preferred_age)


async def process_invalid_self_decription(message: Message):
    await message.reply("Слишном длинное описание")
