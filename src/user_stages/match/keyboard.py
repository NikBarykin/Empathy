"""Inline keyboard for matching stage"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton)

from utils.dummy import DummyCallbackFactory

from .callback_factory import RatingCallbackFactory

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

    partner_score_percent = round(partner_score * 100)
    # We don't want user's to see low values, but for convenience it would be slightly different for different targets
    partner_score_percent = max(partner_score_percent, 40 + (target_id % 10 - 5))

    builder.row(
        InlineKeyboardButton(
            text=f"соответствие {partner_score_percent}%",
            callback_data=DummyCallbackFactory().pack()
        )
    )

    return builder.as_markup()


def get_rated_kb(liked: bool) -> InlineKeyboardMarkup:
    """Keyboard that shows after user rated profile"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=(LIKE_TEXT if liked else DISLIKE_TEXT),
        callback_data=DummyCallbackFactory()
    )
    return keyboard.as_markup()
