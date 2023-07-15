from .config import SELF_DESCRIPTION_MAX_LEN
from .base import Base, CleanModel
from typing import Set

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY


class UserData(Base, CleanModel):
    __tablename__ = "user_data"

    polymorphic_discriminator: Mapped[str]#  = mapped_column(default="user")

    __mapper_args__ = {
        "polymorphic_on": "polymorphic_discriminator",
        "polymorphic_identity": "user_data",
    }

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
    interests: Mapped[Set[str]] = mapped_column(ARRAY(String(32)))
    photo: Mapped[str]
    self_description: Mapped[str] = mapped_column(
        String(SELF_DESCRIPTION_MAX_LEN))

    # TODO: exact types
    min_preferred_age: Mapped[int]
    max_preferred_age: Mapped[int]
    preferred_partner_interests: Mapped[Set[str]] = mapped_column(ARRAY(String(32)))

    # waiting for new users to register
    in_waiting_pool: Mapped[bool] = mapped_column(default=False)
