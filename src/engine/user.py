"""Every helpful function about User-model"""
from logging import Logger
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stages.stage import Stage
from db.user import User


async def get_user_by_id_with_session(id: int, session: AsyncSession) -> User:
    stmt = select(User).where(User.id == id)
    async with session.begin():
        result = await session.execute(stmt.limit(1))
    return result.scalars().one()


async def get_user_by_id(id: int) -> User:
    """
        Search in database for user with given id.
        Raises an exception if can't find user.
    """
    async with Stage.async_session() as session:
        return await get_user_by_id_with_session(id=id, session=session)


async def update_field(
    id: int,
    field_name: str,
    value: Any,
) -> None:
    async with Stage.async_session() as session:
        user = await get_user_by_id_with_session(id=id, session=session)
        async with session.begin():
            setattr(user, field_name, value)


async def submit_user(user: User, logger: Logger | None):
    """Insert user into database"""
    async with Stage.async_session() as session:
        async with session.begin():
            session.add(user)
    if logger is not None:
        logger.debug("Successfully submitted %s", user)
