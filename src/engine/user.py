"""Every helpful function about User-model"""
from logging import Logger
from typing import Any

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import class_mapper

from stage import Stage
from database.user import User


async def __get_user_by_id_with_session_impl(id: int, session: AsyncSession) -> ScalarResult[User]:
    stmt = select(User).where(User.id == id)
    async with session.begin():
        result = await session.execute(stmt.limit(1))
    return result.scalars()


async def get_user_by_id_with_session(id: int, session: AsyncSession) -> User:
    return (await __get_user_by_id_with_session_impl(id, session)).one()


async def get_user_or_none_by_id_with_session(
    id: int,
    session: AsyncSession,
) -> User | None:
    return (await __get_user_by_id_with_session_impl(id, session)).one_or_none()


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
            # TODO: process AttributeError
            setattr(user, field_name, value)


async def get_field(id: int, field_name: str) -> Any:
    async with Stage.async_session() as session:
        user = await get_user_by_id_with_session(id=id, session=session)
        return getattr(user, field_name)


async def submit_user(user: User, logger: Logger | None) -> None:
    """Insert user into database"""
    try:
        async with Stage.async_session() as session:
            async with session.begin():
                session.add(user)
        if logger is not None:
            logger.info(
                "Successfully submitted user %s", user)
    except IntegrityError as e:
        if logger is not None:
            logger.info("user with id %s already exists", user.id)


async def reset_fields(user_id: int) -> None:
    """
        If there is a user with user_id in database
        find him and reset all fields that have default values
        (and also set all nullable columns to NULL).
    """
    async with Stage.async_session() as session:
        user: User | None = (
            await get_user_or_none_by_id_with_session(user_id, session))
        if user is None:
            # User with user_id doesn't exist
            return

        mapper = class_mapper(User)

        async with session.begin():
            for col in mapper.columns:
                # reset field that have default values or nullable
                if col.default is not None:
                    setattr(user, col.key, col.default.arg)
                elif col.nullable:
                    setattr(user, col.key, None)


async def reset_metadata(user_id: int) -> None:
    """Reset user's metadata such as 'frozen'-field"""
    async with Stage.async_session() as session:
        user = await get_user_by_id_with_session(id=user_id, session=session)
        async with session.begin():
            user.frozen = False
            user.blocked_bot = False
            user.in_waiting_pool=False
