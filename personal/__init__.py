# TODO: move everything to __init__.py
# import sys; sys.path.append("..")
from user_state import UserState

from personal.name import process_name
from personal.age import process_age, process_invalid_age
from personal.sex import process_sex, process_invalid_sex
from personal.city import process_city, process_invalid_city
from personal.relationship_goal import (
        process_relationship_goal,
        process_invalid_relationship_goal,
        )
from personal.photo import process_photo
from personal.self_description import (
        process_self_description,
        process_invalid_self_decription,
        )


from constants import (
        SEXES,
        CITIES,
        RELATIONSHIP_GOALS,
        INTERESTS,
        )

from aiogram import Router, F


router = Router()

router.message.register(
        process_name,
        # TODO: name check
        F.text,
        UserState.name,
        )

router.message.register(
        process_age,
        # TODO: check
        F.text.isnumeric(),
        UserState.age,
        )

router.message.register(
        process_invalid_age,
        UserState.age,
        )

router.message.register(
        process_sex,
        F.text.lower().in_(SEXES),
        UserState.sex,
        )

router.message.register(
        process_invalid_sex,
        UserState.sex,
        )

router.message.register(
        process_city,
        F.text.lower().in_(CITIES),
        UserState.city,
        )

router.message.register(
        process_invalid_city,
        UserState.city,
        )

router.message.register(
        process_relationship_goal,
        F.text.lower().in_(RELATIONSHIP_GOALS),
        UserState.relationship_goal,
        )

router.message.register(
        process_invalid_relationship_goal,
        UserState.relationship_goal,
        )


router.message.register(
        process_photo,
        UserState.photo,
        )

router.message.register(
        process_self_description,
        F.text.len() <= 240,
        UserState.self_description,
        )

router.message.register(
        process_invalid_self_decription,
        UserState.self_description,
        )
