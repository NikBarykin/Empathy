from typing import Type

from sqlalchemy import SQLColumnExpression, func, select

from database.user import User

from .score_subexpr import ScoreSubexpr


class InterestsSubexpr(ScoreSubexpr):
    max_possible_score: float = 50

    @staticmethod
    def __count_interests_matching_expr_impl(
        shooter: Type[User],
        aim: User,
    ) -> SQLColumnExpression[float]:
        """
            Pass through shooter.interests and check
            whether it is presented in aim.interests
        """
        shooter_interests = func.unnest(shooter.interests).alias("shooter_interests")
        return (
            select(func.count())
            .select_from(shooter_interests)
            .where(
                shooter_interests.column.in_(aim.interests)
            )
            .label("matching_interests_count")
        )

    @staticmethod
    def __count_interests_matching_expr(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        if isinstance(actor, User):
            return InterestsSubexpr.__count_interests_matching_expr_impl(
                shooter=target, aim=actor)
        elif isinstance(target, User):
            return InterestsSubexpr.__count_interests_matching_expr_impl(
                shooter=actor, aim=target)
        else:
            raise ValueError(f"Bad types actor: {type(actor)}, target: {type(target)}")

    @staticmethod
    def __interests_length_expr(user: User | Type[User]) -> SQLColumnExpression[int]:
        if isinstance(user, User):
            return len(user.interests or [])
        else:
            return func.array_length(user.interests, 1)

    @staticmethod
    def __matching_interests_scaled_expr(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        return (
            InterestsSubexpr.__count_interests_matching_expr(actor, target)
            /
            InterestsSubexpr.__interests_length_expr(actor)
        )

    @staticmethod
    def process(
        actor: User | Type[User],
        target: Type[User] | User,
    ) -> SQLColumnExpression[float]:
        return func.pow(
            InterestsSubexpr.max_possible_score,
            InterestsSubexpr.__matching_interests_scaled_expr(actor, target)
        )
