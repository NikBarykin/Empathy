from typing import Type
from sqlalchemy import SQLColumnExpression
from database.user import User


def sex_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[bool]:
    return target.sex != actor.sex
