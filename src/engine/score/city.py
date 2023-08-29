from typing import Type

from sqlalchemy import SQLColumnExpression, case

from database.user import User

from .score_subexpr import ScoreSubexpr


class CitySubexpr(ScoreSubexpr):
    max_possible_score = 0

    @staticmethod
    def process(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        return case(
            (target.city==actor.city, CitySubexpr.max_possible_score),
            else_=-100
        )
