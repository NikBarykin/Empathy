"""Callback-factories for VerificationStage"""
from aiogram.filters.callback_data import CallbackData


class VerifiedCallbackFactory(CallbackData, prefix="verified"):
    user_id: int


class ResetProfileCallbackFactory(CallbackData, prefix="reset_profile"):
    user_id: int
