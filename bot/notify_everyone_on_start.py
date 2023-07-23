from stage import Stage
from db.user import User

from sqlalchemy import select


async def notify_everyone_on_start(text: str) -> None:
    stmt = select(User.id)
    async with Stage.async_session() as session:
        ids = (await session.execute(stmt)).scalars()
        for user_id in ids:
            await Stage.bot.send_message(user_id, text=text)
