from typing import Type
from sqlalchemy import SQLColumnExpression, case, or_
from database.user import User
from .score_subexpr import ScoreSubexpr


class RelationshipGoalSubexpr(ScoreSubexpr):
    max_possible_score: float = 25

    @staticmethod
    def process(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        return case(
            (or_(actor.relationship_goal==None,
                 target.relationship_goal ==None), 0),
            else_=case(
                (
                    target.relationship_goal == actor.relationship_goal,
                    RelationshipGoalSubexpr.max_possible_score
                ),
                else_=-25
            )
        )
