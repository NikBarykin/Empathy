from typing import Type

from sqlalchemy import SQLColumnExpression, case

from db.user import User


def city_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[float]:
    return case(
        (target.city==actor.city, 0),
        else_=-100
    )
