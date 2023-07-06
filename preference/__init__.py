from user_state import UserState
from preference.min_preferred_age import process_min_preferred_age
from preference.max_preferred_age import process_max_preferred_age

from aiogram import Router
from aiogram import F


router = Router()

router.message.register(
        process_min_preferred_age,
        F.text.isnumeric(),
        UserState.min_preferred_age,
        )

router.message.register(
        process_max_preferred_age,
        F.text.isnumeric(),
        UserState.max_preferred_age
        )
