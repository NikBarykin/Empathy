from typing import Type
import sqlalchemy as sa
from database.user import User
from database.rating import Rating


def rated_expr(
    actor: User | Type[User],
    target: Type[User] | User,
    liked: None | bool = None,
) -> sa.SQLColumnExpression[bool]:
    """
        Check that actor liked or disliked target.
        If liked set to None, just check whether rated.
    """
    liked_expr = (Rating.liked==liked if liked is not None
                  else True)

    if isinstance(target, User):
        return actor.forward_ratings.any(
            sa.and_(Rating.target_id==target.id, liked_expr))
    elif isinstance(actor, User):
        return target.backward_ratings.any(
            sa.and_(Rating.actor_id==actor.id, liked_expr))
    else:
        raise ValueError(f"Bad types: {type(actor)}, {type(target)}")


def liked_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> sa.SQLColumnExpression[bool]:
    return rated_expr(actor, target, True)


def disliked_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> sa.SQLColumnExpression[bool]:
    return rated_expr(actor, target, False)
