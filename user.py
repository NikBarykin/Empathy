from __future__ import annotations

# from rating import Rating

from typing import (
        Set,
        List,
        )
from database_declarative_base import Base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO: get read off
    telegram_id: Mapped[int]
    telegram_handle: Mapped[str]
    name: Mapped[str]
    age: Mapped[int]
    # TODO:
    sex: Mapped[str]
    city: Mapped[str]

    relationship_goal: Mapped[str]
    # interests: Mapped[List[str]]
    photo: Mapped[str]
    self_description: Mapped[str]

    min_preferred_age: Mapped[int]
    max_preferred_age: Mapped[int]

    # TODO: optimize (get rid of first coord)
    # forward_ratings: Mapped[Set["Rating"]] = relationship(back_populates="subject")
    # backward_ratings: Mapped[Set["Rating"]] = relationship(back_populates="object")

    # TODO?: height and weight

    # def rated_with_value(self, obj: User, liked: bool) -> bool:
    #     "whether obj in self's ratings with value <liked> or not"
    #     target_rating = Rating(
    #             liked=liked,
    #             subj_id=self.id,
    #             obj_id=obj.id,
    #             )

    #     return target_rating in self.ratings

    # def is_rated_by(self, obj: User) -> bool:
    #     return obj.rated_with_value(self, true) or obj.rated_with_value(self, false)


    # def rated_any_value(self, obj: User) -> bool:
    #     return self.rated_with_value(obj, True) or self.rated(obj, False)


    def from_fsm_data(fsm_state_data) -> User:
        # TODO:
        argument_names = (
                "telegram_id",
                "telegram_handle",
                "name",
                "age",
                "sex",
                "city",
                "relationship_goal",
                "photo",
                "self_description",
                "min_preferred_age",
                "max_preferred_age",
                )

        return User(**{arg_name:fsm_state_data[arg_name] for arg_name in argument_names})
