from db.base import Base
from db.user_data import UserData

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

    subject: Mapped["UserData"] = relationship(
            primaryjoin=subj_id == UserData.id, backref="forward_ratings")
    object: Mapped["UserData"] = relationship(
            primaryjoin=obj_id == UserData.id, backref="backward_ratings")

    def __init__(self, liked: bool, subj: UserData, obj: UserData):
        self.liked = liked
        self.subject = subj
        self.object = obj
