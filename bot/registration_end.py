from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.user import User
from matching.match import get_next_match
from user_state import UserState


async def process_end(
    bot: Bot,
    user_telegram_id: int,
    state: FSMContext,
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    data = await state.get_data()
    user = User.from_fsm_data(data)

    async with async_session() as session:
        async with session.begin():
            session.add(user)

    await get_next_match(
        bot,
        user_telegram_id,
        async_session,
    )
    await state.set_state(UserState.registered)
