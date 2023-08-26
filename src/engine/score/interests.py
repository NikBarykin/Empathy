from typing import Type
from sqlalchemy import SQLColumnExpression, func, select
from db.user import User


def __count_interests_matching_expr_impl(
    shooter: Type[User],
    aim: User,
) -> SQLColumnExpression[float]:
    """
        Pass through shooter.interests and check
        whether it is presented in aim.interests
    """
    shooter_interests = func.unnest(shooter.interests).alias("shooter_interests")
    return (
        select(func.count())
        .select_from(shooter_interests)
        .where(
            shooter_interests.column.in_(aim.interests)
        )
        .label("matching_interests_count")
    )


def __count_interests_matching_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[float]:
    if isinstance(actor, User):
        return __count_interests_matching_expr_impl(
            shooter=target, aim=actor)
    elif isinstance(target, User):
        return __count_interests_matching_expr_impl(
            shooter=actor, aim=target)
    else:
        raise ValueError(f"Bad types actor: {type(actor)}, target: {type(target)}")


def __interests_length_expr(user: User | Type[User]) -> SQLColumnExpression[int]:
    if isinstance(user, User):
        return len(user.interests or [])
    else:
        return func.array_length(user.interests, 1)


def interests_score_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[float]:
    return func.pow(
        50, __count_interests_matching_expr(actor, target) / __interests_length_expr(actor))
