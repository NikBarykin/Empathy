# for following imports to work
import sys
# TODO: fix
sys.path.append("../empathy")

from database_declarative_base import Base
from user import User

from constants import (
        SEXES,
        CITIES,
        RELATIONSHIP_GOALS,
        )

from generate.config import (
        NO_USERS,
        MIN_AGE,
        MAX_AGE,
        MALE_NAMES,
        FEMALE_NAMES,
        MALE_PHOTOS,
        FEMALE_PHOTOS,
        MALE_SELF_DESCRIPTIONS,
        FEMALE_SELF_DESCRIPTIONS,
        )

import random

from sqlalchemy import (
        create_engine,
        )
from sqlalchemy.orm import (
        Session,
        )


engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine, checkfirst=False)


for i in range(NO_USERS):
    telegram_id = i
    telegram_handle = "imaginary_handle"
    sex = random.choice(SEXES)
    age = random.randint(MIN_AGE, MAX_AGE)

    if sex == "мужчина":
        names = MALE_NAMES
        photos = MALE_PHOTOS
        descriptions = MALE_SELF_DESCRIPTIONS
    elif sex == "женщина":
        names = FEMALE_NAMES
        photos = FEMALE_PHOTOS
        descriptions = FEMALE_SELF_DESCRIPTIONS
    else:
        raise Exception("Unexpected sex value during generation")

    user = User(
            telegram_id=i,
            telegram_handle=telegram_handle,
            name=random.choice(names),
            age=age,
            sex=sex,
            city=random.choice(CITIES),
            relationship_goal=random.choice(RELATIONSHIP_GOALS),
            photo=random.choice(photos),
            self_description=random.choice(descriptions),
            min_preferred_age=0,
            max_preferred_age=100,
            )

    with Session(engine) as session:
        session.add(user)
        session.commit()
