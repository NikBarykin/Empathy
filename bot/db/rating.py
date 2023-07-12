from db.base import Base
from db.user import User

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Rating(Base):
    __tablename__ = "ratings_data"

    liked: Mapped[bool]

    subj_id: Mapped[int] = mapped_column(
            ForeignKey("user_data.id"),
            primary_key=True,
            )

    obj_id: Mapped[int] = mapped_column(
            ForeignKey("user_data.id"),
            primary_key=True,
            )

    subject: Mapped["User"] = relationship(
            primaryjoin=subj_id == User.id, backref="forward_ratings")
    object: Mapped["User"] = relationship(
            primaryjoin=obj_id == User.id, backref="backward_ratings")

    def __init__(self, liked: bool, subj: User, obj: User):
        self.liked = liked
        self.subject = subj
        self.object = obj
