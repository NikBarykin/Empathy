from user_state import UserState
from aiogram.filters import Text


# from matching.match import (
#         process_match,
#         process_anticipate_match,
#         )
from matching.callback_rated import (
        process_callback_rated,
        process_callback_already_rated,
        )
from matching.rating_callback_factory import RatingCallbackFactory

from aiogram import Router


router = Router()

# router.message.register(
#         process_match,
#         Text("match"),
#         UserState.registered,
#         )
# 
# router.message.register(
#         process_anticipate_match,
#         Text("match"),
#         UserState.rates,
#         )


router.callback_query.register(
        process_callback_rated,
        RatingCallbackFactory.filter(),
        UserState.registered,
        )

router.callback_query.register(
        process_callback_already_rated,
        Text("already_rated"),
        )
