"""Callback-factory for interests-stage"""
from aiogram.filters.callback_data import CallbackData


class CheckInterestCallbackFactory(CallbackData, prefix="check_interest"):
    """Is created when user checks one interest"""
    interest: str


class SubmitCallbackFactory(CallbackData, prefix="submit_interests"):
    """Callback factory for submiting interests"""
