from db.user import User
from user_state import UserState

import registration_end

from aiogram import (
        types,
        Bot,
        )
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )


async def process_max_preferred_age(
        message: types.Message,
        bot: Bot,
        state: FSMContext,
        async_session: async_sessionmaker[AsyncSession],
        ):
    await state.update_data(max_preferred_age=int(message.text))

    data = await state.get_data()
    user = User.from_fsm_data(data)

    async with async_session() as session:
        async with session.begin():
            session.add(user)

    await registration_end.process_end(
            bot,
            message.from_user.id,
            state,
            async_session,
            )
