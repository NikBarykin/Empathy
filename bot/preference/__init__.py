from aiogram import F, Router
from aiogram.filters import Text
from interests.check_interest import process_callback_check_interest
from interests.prepare import process_callback_go_page
from interests.submit import (process_callback_submit,
                              process_callback_submit_same)
from user_state import UserState

from preference.max_preferred_age import process_max_preferred_age
from preference.min_preferred_age import process_min_preferred_age

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

router.callback_query.register(
    process_callback_check_interest,
    Text(startswith="interest_"),
    UserState.preferred_partner_interests,
)

router.callback_query.register(
    process_callback_go_page,
    Text(startswith="gopage"),
    UserState.preferred_partner_interests,
)

router.callback_query.register(
    process_callback_submit,
    Text("submit_interests"),
    UserState.preferred_partner_interests,
)

router.callback_query.register(
    process_callback_submit_same,
    Text("submit_interests_same"),
    UserState.preferred_partner_interests,
)
