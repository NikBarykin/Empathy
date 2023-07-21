from __future__ import annotations

import logging

from constants import NEUTRAL_REL_GOAL, NO_INTERESTS
from sqlalchemy import SQLColumnExpression, case, func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.hybrid import hybrid_method

from aiogram.fsm.context import FSMContext

from .user_data import UserData
from .rating import Rating

# Stages
# Personal
from personal.name import NameStage
from personal.age import AgeStage
from personal.sex import SexStage
from personal.city import CityStage
from personal.relationship_goal import RelationshipGoalStage
from interests.preferred_interests import PreferredInterestsStage
from personal.photo import PhotoStage
from personal.self_description import SelfDescriptionStage

# Preferences
from preference.min_preferred_age import MinPreferredAgeStage
from preference.max_preferred_age import MaxPreferredAgeStage
from interests.personal_interests import PersonalInterestsStage

from typing import Dict


class User(UserData):
    __tablename__ = "user_data"
    __mapper_args__ = {"polymorphic_identity": "user"}

    @staticmethod
    def from_fsm_data(data: Dict[str, Any]) -> User:
        fields_and_stages = {
            "name": NameStage,
            "age": AgeStage,
            "sex": SexStage,
            "city": CityStage,
            "relationship_goal": RelationshipGoalStage,
            "interests": PreferredInterestsStage,
            "photo": PhotoStage,
            "self_description": SelfDescriptionStage,
            # preference
            "min_preferred_age": MinPreferredAgeStage,
            "max_preferred_age": MaxPreferredAgeStage,
            "preferred_partner_interests": PreferredInterestsStage,
        }
        return User(
            id=data['id'],
            telegram_handle=data['handle'],
            **{field: data[stage.name]
               for field, stage in fields_and_stages.items()},
        )

    # @staticmethod
    # def from_fsm_state(state: FSMContext) -> User:
    #     return User(
    #         telegram_id=get_id(state),

    #     )
    #     # TODO:
    #     argument_names = (
    #         "telegram_id",
    #         "telegram_handle",
    #         "name",
    #         "age",
    #         "sex",
    #         "city",
    #         "relationship_goal",
    #         "interests",
    #         "photo",
    #         "self_description",
    #         "min_preferred_age",
    #         "max_preferred_age",
    #         "preferred_partner_interests",
    #     )

    #     return User(**{arg_name: fsm_state_data[arg_name] for arg_name in argument_names})

    @hybrid_method
    def __get_relationship_goal_score_as_partner_of(self, subject: User) -> float:
        if subject.relationship_goal == NEUTRAL_REL_GOAL or self.relationship_goal == NEUTRAL_REL_GOAL:
            return 0

        if self.relationship_goal == subject.relationship_goal:
            # for goal overlap we get plus 25
            return +25
        else:
            # and if goals doesn't overlap we get minus 25
            return -25

    @__get_relationship_goal_score_as_partner_of.expression
    @classmethod
    def __get_relationship_goal_score_as_partner_of(
        cls, subject: User) -> SQLColumnExpression[float]:
        return case(
            (or_(subject.relationship_goal == NEUTRAL_REL_GOAL,
                 cls.relationship_goal == NEUTRAL_REL_GOAL), 0),
            else_=case(
                (cls.relationship_goal == subject.relationship_goal, +25),
                else_=-25
            )
        )

    @hybrid_method
    def __get_number_of_interests_matching_with_preferences_of(
        self, subject: User) -> int:
        return len(self.interests.intersection(subject.preferred_partner_interests))

    # TODO: mark 'inline'
    @__get_number_of_interests_matching_with_preferences_of.expression
    @classmethod
    def __get_number_of_interests_matching_with_preferences_of(
        cls, subject: User) -> SQLColumnExpression[int]:
        interests_view = func.unnest(cls.interests).alias("interests_view")
        return (
            select(func.count())
            .select_from(interests_view)
            .where(
                interests_view.column.in_(subject.preferred_partner_interests)
                # subject.preferred_partner_interests.contains(interests_view)
            )
            .label("same_interests_count")
        )

    @hybrid_method
    def __get_number_of_interests_matching_with_preferences_of_scaled(
        self, subject: User) -> float:
        return self.__get_number_of_interests_matching_with_preferences_of(subject) / NO_INTERESTS

    @hybrid_method
    def __get_interests_score_as_partner_of(self, subject: User) -> float:
        return 50 ** self.__get_number_of_interests_matching_with_preferences_of_scaled(subject)

    @__get_interests_score_as_partner_of.expression
    @classmethod
    def __get_interests_score_as_partner_of(cls, subject: User) -> SQLColumnExpression[float]:
        return func.pow(50, cls.__get_number_of_interests_matching_with_preferences_of_scaled(subject))

    @hybrid_method
    def get_partner_score(self, subject: User) -> float:
        return (
            self.__get_interests_score_as_partner_of(subject)
            +
            self.__get_relationship_goal_score_as_partner_of(subject)
        )

    @hybrid_method
    def __is_eligible_age_for(self, subject: User) -> bool:
        return (
            (self.age >= subject.min_preferred_age)
            &
            (self.age <= subject.max_preferred_age)
        )

    @hybrid_method
    def __is_eligible_sex_for(self, subject: User) -> bool:
        return self.sex != subject.sex

    @hybrid_method
    def __is_not_rated_by(self, subject: User) -> bool:
        return all([r.subj_id != subject.id for r in self.backward_ratings])

    @__is_not_rated_by.expression
    @classmethod
    def __is_not_rated_by(cls, subject: User) -> SQLColumnExpression[bool]:
        return ~cls.backward_ratings.any(Rating.subj_id == subject.id)

    @hybrid_method
    def is_eligible_candidate_for(self, subject: User) -> bool:
        return (
            (self.__is_eligible_age_for(subject))
            &
            (self.__is_eligible_sex_for(subject))
            &
            (self.__is_not_rated_by(subject))
        )

    async def insert_to(
        self,
        async_session: async_sessionmaker[AsyncSession],
    ) -> None:
        async with async_session() as session:
            async with session.begin():
                await session.merge(self)

        # async with async_session() as session:
        #     async with session.begin():
        #         await session.merge(self)

        async with async_session() as session:
            stmt = select(User).where(User.id==self.id)
            found_user = (await session.execute(stmt)).scalars().one()
            logging.info(f"expected_user: {self}")
            logging.info(f"found_user: {found_user}")

    @staticmethod
    async def get_by_telegram_id(
        telegram_id: int,
        session: AsyncSession,
    ) -> User:
        stmt = select(User).where(User.id == telegram_id)
        async with session.begin():
            result = await session.execute(stmt.limit(1))
        return result.scalars().one()

    @staticmethod
    async def put_in_waiting_pool(
        telegram_id: int,
        async_session: async_sessionmaker[AsyncSession],
    ) -> None:
        async with async_session() as session:
            user: User = await User.get_by_telegram_id(telegram_id, session)
            logging.debug(f"{user.name} was put in a waiting pool")
            async with session.begin():
                user.in_waiting_pool = True
