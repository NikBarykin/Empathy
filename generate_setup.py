from user import User
from constants import (
        SEXES,
        CITIES,
        RELATIONSHIP_GOALS,
        )

from generate.config import (
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

from sqlalchemy import engine


for i in range(NO_USERS):
    telegram_id = i
    telegram_handle = "imaginary_handle"
    sex = random.choice(SEXES)
    age = random.randint(MIN_AGE, MAX_AGE)

    if sex == "мужчина":
        names = MALE_NAMES
        photos = MALE_PHOTOS
        descriptions = MALE_SELF_DESCRIPTIONS
    else:
        names = FEMALE_NAMES
        photos = FEMALE_PHOTOS
        descriptions = FEMALE_SELF_DESCRIPTIONS

    user = User(
            telegram_id=i,
            telegram_handle=telegram_handle,
            name=random.choice(names),
            age=age,
            sex=sex,
            city=random.choice(CITIES),
            relationship_goal=random.choice(RELATIONSHIP_GOALS),
            photo=random.choice(photos),
            self_descriptions=random.choice(descriptions),
            min_preferred_age=0,
            max_preferred_age=100,
            )

    










NAMES = MALE_NAMES + FEMALE_NAMES

NO_AGENTS = 10

lines = []

for i in range (NO_AGENTS):
    name = random.choice(NAMES)
    age = random.randint(MIN_AGE, MAX_AGE)

    if name in MALE_NAMES:
        gender = "мужчина"
        pictures = MALE_PICTURES
        description = random.choice(MALE_SELF_DESCRIPTIONS)
    else:
        gender = "женщина"
        pictures = FEMALE_PICTURES
        description = random.choice(FEMALE_SELF_DESCRIPTIONS)

    agent = Agent(
            i,
            "username",
            name,
            age,
            gender,
            random.choice(AVAILABLE_CITIES),
            random.choice(pictures),
            description,
            -1,
            -1,
            )

    lines.append(agent.serialize())

with open("setup.txt", "w", encoding="utf-8") as f:
    f.writelines('\n'.join(lines))
