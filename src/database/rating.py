"""A rating that users create for each other"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .user import User


class Rating(Base):
    __tablename__ = "rating_data"

    liked: Mapped[bool]

    actor_id: Mapped[int] = mapped_column(
            ForeignKey("user_data.id"),
            primary_key=True,
            )

    target_id: Mapped[int] = mapped_column(
            ForeignKey("user_data.id"),
            primary_key=True,
            )

    actor: Mapped["User"] = relationship(
            primaryjoin=actor_id == User.id, backref="forward_ratings")
    target: Mapped["User"] = relationship(
            primaryjoin=target_id == User.id, backref="backward_ratings")

    def __repr__(self) -> str:
        return f"Rating(liked={self.liked}, actor_id={self.actor_id}, target_id={self.target_id})"
