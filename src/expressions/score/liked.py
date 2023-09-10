from typing import Type
from sqlalchemy import SQLColumnExpression, case
from database.user import User
from expressions.rated import liked_expr, disliked_expr
from .score_subexpr import ScoreSubexpr


class LikedSubexpr(ScoreSubexpr):
    max_possible_score = 25

    @staticmethod
    def process(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        return case(
            (liked_expr(target, actor), LikedSubexpr.max_possible_score),
            else_=case(
                (disliked_expr(target, actor), -15),
                else_=0
            )
        )
