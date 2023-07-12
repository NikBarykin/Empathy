from user import User
from rating import Rating

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )


async def check_liked(
        subj: User,
        obj: User,
        session: AsyncSession) -> bool:
    """
    whether obj in subj's likes or not
    """
    stmt = (
            select(Rating)
            .where(Rating.liked==True)
            .where(Rating.subject == subj)
            .where(Rating.object == obj)
            .limit(1)
            )
    result = await session.execute(stmt)
    return result.scalars().first() is not None


# TODO: optimize
async def get_user_by_telegram_id(
        telegram_id: int,
        session: AsyncSession,
        ) -> User:
    stmt = select(User).where(User.telegram_id == telegram_id)
    async with session.begin():
        result = await session.execute(stmt.limit(1))
    return result.scalars().one()


async def get_match_by_user(
        subject: User,
        session: AsyncSession,
        ) -> Optional[User]:
    stmt = (
            select(User)
            .where(User.id != subject.id)
            .where(User.sex != subject.sex)
            .where(~User.backward_ratings.any(Rating.subj_id == subject.id))
            .where(User.age >= subject.min_preferred_age)
            .where(User.age <= subject.max_preferred_age)
            )
    result = await session.execute(stmt.limit(1))
    return result.scalars().one_or_none()


async def find_match(
        telegram_id: int,
        async_session: async_sessionmaker[AsyncSession],
        ) -> Optional[User]:

    async with async_session() as session:
        subject = await get_user_by_telegram_id(telegram_id, session)

        result = await get_match_by_user(subject, session)

        return result