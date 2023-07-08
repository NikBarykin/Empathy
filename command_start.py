from user import User
from user_state import UserState

import registration_end

from aiogram import (
        types,
        Bot,
        )
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )
from sqlalchemy import select


router = Router()

async def user_already_in_database(
        telegram_id: int,
        async_session: async_sessionmaker[AsyncSession],
        ) -> bool:
    async with async_session() as session:
        stmt = select(User.id).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        return result.scalars().first() is not None


@router.message(Command('start'))
async def process_command_start(
        message: types.Message,
        bot: Bot,
        state: FSMContext,
        async_session: async_sessionmaker[AsyncSession],
        ):
    telegram_id = message.from_user.id

    # TODO: better answers
    if await user_already_in_database(telegram_id, async_session):
        await registration_end.process_end(
                bot,
                message.from_user.id,
                state,
                async_session,
                )

    else:
        await state.update_data(telegram_id=telegram_id)
        await state.update_data(telegram_handle=message.from_user.username)

        await message.answer("Как тебя зовут?")
        await state.set_state(UserState.name)
