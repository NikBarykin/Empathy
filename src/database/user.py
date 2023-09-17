from typing import Set, List, Dict, Any, Optional

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa

from .base import Base, CleanModel


MAX_BIO_SZ: int = 1000
MIN_AGE: int = 16
MAX_AGE: int = 100
MAX_NAME_SZ: int = 64


class User(Base, CleanModel):
    """Model for a user of bot"""

    __tablename__ = "user_data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    name: Mapped[Optional[str]] = mapped_column(
        String(MAX_NAME_SZ), nullable=True)

    age: Mapped[Optional[int]]
    sex: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    photo: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]
    interests: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String(64)), nullable=True)

    relationship_goal: Mapped[Optional[str]]

    min_partner_age: Mapped[int] = mapped_column(sa.Integer, default=MIN_AGE)
    max_partner_age: Mapped[int] = mapped_column(sa.Integer, default=MAX_AGE)

    # metainformation
    # TODO: move to other class
    in_waiting_pool: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    blocked_bot: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    frozen: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    verified: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    reported_cnt: Mapped[int] = mapped_column(sa.Integer, default=0)

    # TODO:
    @hybrid_property
    def registered(self) -> bool:
        REQUIRED_FIELDS = (
            "name", "age", "sex", "city", "photo", "bio", "interests")

        result = True
        for fieldname in REQUIRED_FIELDS:
            # It is important to "adjust" result as as right argument for '&'
            # (it doesn't work other way)
            result = (getattr(self, fieldname) != None) & result
        return result

    def __repr__(self) -> str:
        return (
            "<{0.__class__.__name__}("
            "frozen={0.frozen}, "
            "verified={0.verified}, "
            "reported_cnt={0.reported_cnt}, "
            "id={0.id}, "
            "age={0.age}, "
            "sex={0.sex}, "
            "city={0.city}, "
            "photo={0.photo}, "
            "bio={0.bio}, "
            "interests={0.interests}, "
            ")>"
        ).format(self)
