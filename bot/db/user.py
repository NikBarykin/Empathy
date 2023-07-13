from __future__ import annotations

from typing import List, Set

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base, CleanModel
from .config import SELF_DESCRIPTION_MAX_LEN


class User(Base, CleanModel):
    __tablename__ = "user_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO: get reed of
    telegram_id: Mapped[int]
    # get reed of magic number '32'
    telegram_handle: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(32))
    age: Mapped[int]
    # TODO:
    sex: Mapped[str]
    city: Mapped[str]

    relationship_goal: Mapped[str]
    interests: Mapped[List[str]] = mapped_column(ARRAY(String(32)))
    photo: Mapped[str]
    self_description: Mapped[str] = mapped_column(
        String(SELF_DESCRIPTION_MAX_LEN))

    # TODO: exact types
    min_preferred_age: Mapped[int]
    max_preferred_age: Mapped[int]

    @staticmethod
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
            "interests",
            "photo",
            "self_description",
            "min_preferred_age",
            "max_preferred_age",
        )

        return User(**{arg_name:fsm_state_data[arg_name] for arg_name in argument_names})

    # @staticmethod
    # def insert(async_session: async_sessionmaker[AsyncSession]):
    #     async with async_session() as session:
    #         async with session.begin():
    #             session.add(user)
