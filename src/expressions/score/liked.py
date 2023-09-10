from typing import Type
from sqlalchemy import SQLColumnExpression, case
from database.user import User
from expressions.rated import rated_expr
from .score_subexpr import ScoreSubexpr


class LikedSubexpr(ScoreSubexpr):
    max_possible_score = 25

    @staticmethod
    def process(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        return case(
            (rated_expr(actor, target, True), LikedSubexpr.max_possible_score),
            else_=0
        )
