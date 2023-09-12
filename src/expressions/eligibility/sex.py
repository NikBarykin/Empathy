from typing import Type
import sqlalchemy as sa
from database.user import User
from user_stages.field_stages.relationship_goal.constants import COMMUNICATION_GOAL


def sex_expr(
    actor: User | Type[User],
    target: Type[User] | User,
) -> sa.SQLColumnExpression[bool]:
    return sa.or_(
        # if bot users want to communicate (no romantic) we don't care about sex
        sa.and_(
            actor.relationship_goal==COMMUNICATION_GOAL,
            target.relationship_goal==COMMUNICATION_GOAL
        ),
        target.sex != actor.sex
    )
