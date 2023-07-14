from aiogram.fsm.context import FSMContext
# 3rd party
from aiogram.types import Message
from db.config import SELF_DESCRIPTION_MAX_LEN
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from user_state import UserState

## TODO: move to other place
#async def insert_personal(
#        async_session: async_sessionmaker[AsyncSession],
#        personal: Personal,
#        ) -> None:
#    async with async_session() as session:
#        async with session.begin():
#            session.add(personal)


async def prepare(
        message: Message,
        state: FSMContext,
        ):
    # TODO: why 240
    await message.answer(
        f"Напиши немного о себе в свободной форме (не более {SELF_DESCRIPTION_MAX_LEN} символов)")
    await state.set_state(UserState.self_description)


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
