"""Keyboards for interests stage"""
from typing import Iterable
from copy import deepcopy

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.dummy import DummyCallbackFactory

from .constants import (
    INTERESTS, CHECK_TEXT,
    INTERESTS_CHECKED_VERSIONS, NO_BUTTONS_IN_ROW, QUESTION_KB_TEMPLATE)


def get_question_kb(checked_interests: Iterable[str]) -> InlineKeyboardMarkup:
    """Get keyboard for quering user's interests"""
    keyboard = deepcopy(QUESTION_KB_TEMPLATE)

    for i, interest in enumerate(INTERESTS):
        if interest in checked_interests:
            row = i // NO_BUTTONS_IN_ROW
            col = i % NO_BUTTONS_IN_ROW
            keyboard.inline_keyboard[row][col].text = INTERESTS_CHECKED_VERSIONS[i]

    return keyboard


def get_submit_kb(checked_interests: Iterable[str]) -> InlineKeyboardMarkup:
    """Keyboard after submission"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CHECK_TEXT + interest + CHECK_TEXT,
                    callback_data=DummyCallbackFactory().pack(),
                )
            ]
            for interest in checked_interests
        ]
    )
