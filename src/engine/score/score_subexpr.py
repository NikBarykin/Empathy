from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy import SQLColumnExpression

from database.user import User


class ScoreSubexpr(ABC):
    """
        Base class for score-subexpressions.
        Contains max-possible-score that user can get
    """
    max_possible_score: float = None

    @staticmethod
    @abstractmethod
    def process(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        pass
