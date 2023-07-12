from user_state import UserState

from matching.match import get_next_match

from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)


async def process_end(
    bot: Bot,
    user_telegram_id: int,
    state: FSMContext,
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    await get_next_match(
        bot,
        user_telegram_id,
        async_session,
    )
    await state.set_state(UserState.registered)
