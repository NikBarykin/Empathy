from database.user import User

from sqlalchemy import select

from stage import Stage

from engine.user import get_user_by_id_with_session

from expressions.score import partner_score_expr


async def score_partner(actor_id: int, partner_id: int) -> float:
    """Score existing partner with id -- partner_id"""
    async with Stage.async_session() as session:
        actor: User = await get_user_by_id_with_session(
            id=actor_id, session=session)

        stmt = (
            select(partner_score_expr(actor, User))
            .where(User.id==partner_id)
        )

        result = await session.execute(stmt.limit(1))
        return result.scalars().one()
