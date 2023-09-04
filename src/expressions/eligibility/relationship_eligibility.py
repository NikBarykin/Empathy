from typing import Type
from sqlalchemy import SQLColumnExpression
from database.user import User
from .partner_eligibility import partner_eligibility_expr


def relationship_eligibility_expr(
    user1: User | Type[User],
    user2: Type[User] | User,
) -> SQLColumnExpression[bool]:
    """user2 is eligible for user1 and vice versa"""
    return (
        partner_eligibility_expr(user1, user2)
        &
        partner_eligibility_expr(user2, user1)
    )
