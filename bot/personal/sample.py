import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"


from sqlalchemy import create_engine

engine = create_engine("sqlite", echo=True)


Base.metadata.create_all(engine)


from sqlalchemy.orm import Session



with Session(engine) as session:
    nikita = User(name="Nikita")
    katya = User(name="Katya")

    session.add_all([nikita, katya])

    session.commit()
