"""Callback-factory for match-stage"""
from aiogram.filters.callback_data import CallbackData


class RatingCallbackFactory(CallbackData, prefix="rating"):
    liked: bool
    actor_id: int
    target_id: int
