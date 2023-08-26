from typing import Type
from sqlalchemy import SQLColumnExpression, case, or_
from db.user import User


def relationship_goal_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> SQLColumnExpression[float]:
    return case(
        (or_(actor.relationship_goal==None,
             target.relationship_goal ==None), 0),
        else_=case(
            (target.relationship_goal == actor.relationship_goal, +25),
            else_=-25
        )
    )
