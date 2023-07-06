from aiogram.filters.callback_data import CallbackData


class RatingCallbackFactory(CallbackData, prefix="rate"):
    liked: bool
    subj_telegram_id: int
    obj_telegram_id: int
