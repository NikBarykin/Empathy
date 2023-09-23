import sqlalchemy as sa

from database.user import User

from stage import Stage


async def get_unverified_user_id() -> int | None:
    """
        Get any user that isn't verified yet
        and is available for search
        (i.e. didn't block bot and isn't frozen and is registered)
    """
    stmt = (
        sa.select(User.id)
        .where(~User.verified)
        .where(User.registered)
        .where(~User.frozen)
        .where(~User.blocked_bot)
    )

    async with Stage.async_session() as session:
        result = await session.execute(stmt.limit(1))
        return result.scalars().one_or_none()
