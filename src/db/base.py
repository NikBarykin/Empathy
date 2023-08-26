from datetime import datetime

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CleanModel:
    """
        Basic model that contains metainformation
    """
    creation_datetime: Mapped[datetime] = mapped_column(default=datetime.now())
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now())
