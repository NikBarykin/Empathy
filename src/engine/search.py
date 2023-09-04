"""Search for a best partner"""
from sqlalchemy import select

from stage import Stage
from database.user import User

from engine.user import get_user_by_id_with_session

from expressions.score import partner_score_expr
from expressions.eligibility import relationship_eligibility_expr
from expressions.rated import rated_expr


async def find_partner_for(actor_id: int) -> int | None:
    """
        Find the best option for user with actor_id.
        Return None if there is no partner and partner-id otherwise.
    """
    # TODO: optimize
    async with Stage.async_session() as session:
        actor: User = await get_user_by_id_with_session(
            actor_id, session=session)

        stmt = (
            select(User.id)
            .where(relationship_eligibility_expr(actor, User))
            .where(~rated_expr(actor, User))
            .order_by(partner_score_expr(actor, User))
        )

        result = await session.execute(stmt.limit(1))
        return result.scalars().one_or_none()
