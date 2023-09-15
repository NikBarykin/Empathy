from typing import Type, List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.dummy import DummyCallbackFactory
from stage import Stage


def get_keyboard_for_alternatives(
    alternatives: List[Type[Stage]],
) -> InlineKeyboardMarkup:
    """Create inline keyboard that contains buttons with alternative-names"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=stage.name, callback_data=stage.name)]
            for stage in alternatives
        ]
    )


def get_keyboard_for_chosen_alternative(
    chosen_alternative: Type[Stage],
) -> InlineKeyboardMarkup:
    """
        Create inline keyboard with one silent button
        that represents chosen alternative.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=chosen_alternative.name,
                    callback_data=DummyCallbackFactory().pack(),
                )
            ]
        ]
    )
