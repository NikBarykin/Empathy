from user import User
from user_state import UserState
from matching.keyboards import get_reply_kb

from aiogram import types
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
        state: FSMContext,
        async_session: async_sessionmaker[AsyncSession],
        ):
    telegram_id = message.from_user.id

    if await user_already_in_database(telegram_id, async_session):
        await message.answer(
                text="Ты уже зарегистрирован, подбор партнера доступен",
                reply_markup=get_reply_kb(),
                )
        await state.set_state(UserState.registered)

    else:
        await state.update_data(telegram_id=telegram_id)
        await state.update_data(telegram_handle=message.from_user.username)

        await message.answer("Как тебя зовут?")
        await state.set_state(UserState.name)
