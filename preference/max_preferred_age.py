from user import User
from user_state import UserState
from matching.keyboards import get_reply_kb

from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )


async def process_max_preferred_age(
        message: types.Message,
        state: FSMContext,
        async_session: async_sessionmaker[AsyncSession],
        ):
    await state.update_data(max_preferred_age=int(message.text))

    data = await state.get_data()
    user = User.from_fsm_data(data)

    async with async_session() as session:
        async with session.begin():
            session.add(user)

    await message.answer(
            "Ты успешно зарегистрирован! Теперь тебе доступен подбор партнера.",
            reply_markup = get_reply_kb())
    await state.set_state(UserState.registered)

