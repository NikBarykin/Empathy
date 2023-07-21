import sys; sys.path.append("../Empathy")

import asyncio
import random

from generate.gen_config import (FEMALE_NAMES, FEMALE_PHOTOS,
                             FEMALE_SELF_DESCRIPTIONS, MALE_NAMES, MALE_PHOTOS,
                             MALE_SELF_DESCRIPTIONS, MAX_AGE, MIN_AGE,
                             NO_USERS)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from bot.config import DATABASE_URL
from bot.constants import (CITIES, INTERESTS, NO_INTERESTS, RELATIONSHIP_GOALS,
                           SEXES)
from bot.db.base import Base
from bot.db.engine import (construct_async_engine, get_async_sessionmaker,
                           proceed_schemas)
from bot.db.user import User

TELEGRAM_HANDLE = "imaginary_handle"


def generate_user() -> User:
    telegram_id = random.randint(1, 1000000000)
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

    interests = {random.choice(INTERESTS) for _ in range(NO_INTERESTS)}

    return User(
        telegram_id=telegram_id,
        telegram_handle=TELEGRAM_HANDLE,
        name=random.choice(names),
        age=age,
        sex=sex,
        city=random.choice(CITIES),
        relationship_goal=random.choice(RELATIONSHIP_GOALS),
        interests=interests,
        photo=random.choice(photos),
        self_description=random.choice(descriptions),
        min_preferred_age=0,
        max_preferred_age=100,
        preferred_partner_interests=interests,
    )


async def main() -> None:
    engine = construct_async_engine(DATABASE_URL)
    await proceed_schemas(engine=engine, metadata=Base.metadata)
    async_sessionmaker = get_async_sessionmaker(engine)

    users = [generate_user() for _ in range(10000)]

    async with async_sessionmaker() as session:
        async with session.begin():
            session.add_all(users)

    subject: User = users[0]
    print(f"User interests: {subject.preferred_partner_interests}")

    async with async_sessionmaker() as session:
        stmt = (select(User)
                .where(User.is_eligible_candidate_for(subject))
                .where(User.get_partner_score(subject) >= 20)
                .order_by(User.get_partner_score(subject))
                )

        result = (await session.execute(stmt))
        for target in result.scalars():
            print(f"matched interests: {target.interests}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
