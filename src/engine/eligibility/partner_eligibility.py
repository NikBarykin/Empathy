from typing import Type

from sqlalchemy import SQLColumnExpression

from db.user import User

from engine.score import partner_score_expr

from .age import age_expr
from .sex import sex_expr
from .not_rated import not_rated_expr


def partner_eligibility_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[bool]:
    return (
        age_expr(actor, target)
        &
        sex_expr(actor, target)
        &
        not_rated_expr(actor, target)
        &
        target.registered
        &
        (partner_score_expr(actor, target) >= 0)
        # &
        # (~target.frozen)
    )
