"""Keyboards for interests stage"""
from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.dummy import DummyCallbackFactory

from .callback_factory import (
    CheckInterestCallbackFactory, SubmitCallbackFactory)
from .constants import INTERESTS, CHECK_TEXT, SUBMIT_TEXT


def get_question_kb(checked_interests: Iterable[str]) -> InlineKeyboardMarkup:
    """Get keyboard for quering user's interests"""
    builder = InlineKeyboardBuilder()

    for interest in INTERESTS:
        text = interest
        if interest in checked_interests:
            # TODO: optimize by precalc checked versions
            text = CHECK_TEXT + text + CHECK_TEXT
        builder.button(
            text=text,
            callback_data=CheckInterestCallbackFactory(interest=interest),
        )

    builder.adjust(2)

    builder.row(
        InlineKeyboardButton(
            text=SUBMIT_TEXT,
            callback_data=SubmitCallbackFactory().pack(),
        )
    )

    return builder.as_markup()


def get_submit_kb(checked_interests: Iterable[str]) -> InlineKeyboardMarkup:
    """Keyboard after submission"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton
                (
                    text=CHECK_TEXT + interest + CHECK_TEXT,
                    callback_data=DummyCallbackFactory().pack(),
                )
            ]
            for interest in checked_interests
        ]
    )
