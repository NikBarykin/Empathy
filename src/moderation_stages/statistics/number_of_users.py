import sqlalchemy as sa

from stage import Stage
from database.user import User


stmt = sa.select(sa.func.count()).select_from(User)


async def count_users() -> int:
    async with Stage.async_session() as session:
        return (await session.execute(stmt)).scalar()
