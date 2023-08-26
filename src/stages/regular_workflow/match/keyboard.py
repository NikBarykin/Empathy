"""Inline keyboard for matching stage"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from utils.dummy import DummyCallbackFactory

from .rating_callback_factory import RatingCallbackFactory

from .constants import (
    LIKE_TEXT,
    DISLIKE_TEXT,
)


async def get_query_kb(
    actor_id: int,
    target_id: int,
    partner_score: float,
) -> InlineKeyboardMarkup:
    """Keyboard that asks user to rate given profile"""
    builder = InlineKeyboardBuilder()

    builder.button(
            text=LIKE_TEXT,
            callback_data=RatingCallbackFactory(
                liked=True,
                actor_id=actor_id,
                target_id=target_id,
                )
            )

    builder.button(
            text=DISLIKE_TEXT,
            callback_data=RatingCallbackFactory(
                liked=False,
                actor_id=actor_id,
                target_id=target_id,
                )
            )

    builder.adjust(2)
    assert 0 <= partner_score <= 1
    builder.button(
        text=f"соответствие {partner_score * 100}%",
        callback_data=DummyCallbackFactory(),
    )

    return builder.as_markup()


def get_rated_kb(liked: bool) -> InlineKeyboardMarkup:
    """Keyboard that shows after user rated profile"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
            text=(LIKE_TEXT if liked else DISLIKE_TEXT),
            callback_data=DummyCallbackFactory(),
            )
    return keyboard.as_markup()
