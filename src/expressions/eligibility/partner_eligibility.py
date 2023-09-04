from typing import Type

import sqlalchemy as sa

from database.user import User

from expressions.score import partner_score_expr

from .age import age_expr
from .sex import sex_expr
# from .not_frozen import not_frozen_expr
# from .not_blocked_bot import not_frozen_expr


def partner_eligibility_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> sa.SQLColumnExpression[bool]:
    """Is target eligible for actor (does he satisfy actor's preferences)"""
    return (
        age_expr(actor, target)
        &
        sex_expr(actor, target)
        &
        target.registered
        &
        sa.not_(target.frozen)
        &
        sa.not_(target.blocked_bot)
        &
        (partner_score_expr(actor, target) >= 0)
    )
