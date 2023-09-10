from typing import Type
from sqlalchemy import SQLColumnExpression
from database.user import User


def age_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[bool]:
    return (
        (target.age >= actor.min_partner_age)
        &
        (target.age <= actor.max_partner_age)
    )