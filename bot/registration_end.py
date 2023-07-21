import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.user import User
from matching.match import get_next_match
from user_state import UserState


async def notify_waiting_pool(
    bot: Bot,
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    stmt = select(User).where(User.in_waiting_pool==True)
    async with async_session() as session:
        async with session.begin():
            for user in (await session.scalars(stmt)).all():
                logging.debug(f"{user.name} was notified""")
                await get_next_match(
                    bot,
                    user.id,
                    async_session,
                )
                user.in_waiting_pool = False


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
    stmt = select(User).where(User.in_waiting_pool==True)

    await notify_waiting_pool(bot, async_session)
