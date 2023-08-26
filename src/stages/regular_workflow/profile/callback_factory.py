"""Callback-factories for profile-stage"""
from aiogram.filters.callback_data import CallbackData


class GoFreezeCallbackFactory(CallbackData, prefix="go_freeze"):
    """Callback-factory for jumping to freeze-stage"""


class GoUpdateCallbackFactory(CallbackData, prefix="go_update"):
    """Callback-factory for starting updating your profile"""
