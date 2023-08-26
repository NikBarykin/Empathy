from typing import Type

from db.user import User
from sqlalchemy import SQLColumnExpression

from .interests import interests_score_expr
from .relationship_goal import relationship_goal_expr
from .city import city_expr


def partner_score_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[float]:
    return (
        interests_score_expr(actor, target)
        +
        relationship_goal_expr(actor, target)
        +
        city_expr(actor, target)
    )
