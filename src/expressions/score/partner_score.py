from typing import Type

from sqlalchemy import SQLColumnExpression

from database.user import User

from .interests import InterestsSubexpr
from .relationship_goal import RelationshipGoalSubexpr
from .city import CitySubexpr
from .liked import LikedSubexpr


SUBEXPRS = (
    CitySubexpr,
    InterestsSubexpr,
    RelationshipGoalSubexpr,
    LikedSubexpr,
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
