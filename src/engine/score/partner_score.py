from typing import Type


from sqlalchemy import SQLColumnExpression, select

from database.user import User

from stage import Stage

from engine.user import get_user_by_id_with_session

from .interests import InterestsSubexpr
from .relationship_goal import RelationshipGoalSubexpr
from .city import CitySubexpr


SUBEXPRS = (
    CitySubexpr,
    InterestsSubexpr,
    RelationshipGoalSubexpr,
)


def partner_score_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[float]:
    """
        SQL-expression for calculating
        a score of partner -- target for actor
    """
    absolute_score_expr: SQLColumnExpression[float] = 0
    max_possible_score: float = 0

    for subexpr in SUBEXPRS:
        absolute_score_expr = absolute_score_expr + subexpr.process(actor, target)
        max_possible_score += subexpr.max_possible_score

    return absolute_score_expr / max_possible_score


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
