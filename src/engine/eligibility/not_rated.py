from typing import Type
from sqlalchemy import SQLColumnExpression
from database.user import User
from database.rating import Rating


def not_rated_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[bool]:
    """Check that target is not rated by actor"""
    if isinstance(target, User):
        return ~actor.forward_ratings.any(Rating.target_id == target.id)
    elif isinstance(actor, User):
        return ~target.backward_ratings.any(Rating.actor_id == actor.id)
    else:
        raise ValueError(f"Bad types: {type(actor)}, {type(target)}")
