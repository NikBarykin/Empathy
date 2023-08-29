from typing import Type
from sqlalchemy import SQLColumnExpression
from database.user import User


def not_frozen_expr(
    user: User | Type[User]
) -> SQLColumnExpression[bool]:
    """Check that target is not frozen"""
    if isinstance(user, User):
        return not user.frozen
    else:
        return ~user.frozen
