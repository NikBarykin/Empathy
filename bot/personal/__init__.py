from aiogram import F, Router
from aiogram.filters import Text
from constants import CITIES, INTERESTS, RELATIONSHIP_GOALS, SEXES
from interests.check_interest import process_callback_check_interest
from interests.submit import process_callback_submit
from user_state import UserState

from personal.age import process_age, process_invalid_age
from personal.city import process_city, process_invalid_city
from personal.name import process_name
from personal.photo import (ADD_PROFILE_PHOTO_TEXT,
                            process_explicitly_choosen_photo,
                            process_profile_photo)
from personal.relationship_goal import (process_invalid_relationship_goal,
                                        process_relationship_goal)
from personal.self_description import (process_invalid_self_decription,
                                       process_self_description)
from personal.sex import process_invalid_sex, process_sex

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

router.callback_query.register(
        process_callback_check_interest,
        Text(startswith="interest_"),
        UserState.interests,
        )

router.callback_query.register(
        process_callback_submit,
        Text("submit_interests"),
        UserState.interests,
        )


router.message.register(
        process_explicitly_choosen_photo,
        F.photo,
        UserState.photo,
        )

router.message.register(
        process_profile_photo,
        Text(ADD_PROFILE_PHOTO_TEXT),
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
