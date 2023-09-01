"""Search for a best partner"""
import logging

from sqlalchemy import select

from stage import Stage
from database.user import User

from engine.user import get_user_by_id_with_session

from .score import partner_score_expr
from .eligibility import partner_eligibility_expr


async def find_partner_for(actor_id: int):
    """Find the best option for user with actor_id"""
    # TODO: optimize
    async with Stage.async_session() as session:
        actor: User = await get_user_by_id_with_session(
            actor_id, session=session)

        stmt = (
            select(User)
            .where(partner_eligibility_expr(actor, User))
            .where(partner_eligibility_expr(User, actor))
            .order_by(partner_score_expr(actor, User))
        )

        result = await session.execute(stmt.limit(1))
        return result.scalars().one_or_none()
