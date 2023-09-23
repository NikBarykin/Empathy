"""Inline keyboard for VerificationStage"""
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton)

from utils.keyboard import DummyInlineKeyboard

from .callback_factory import VerifiedCallbackFactory, ResetProfileCallbackFactory

from .constants import VERIFY_BUTTON_TEXT, RESET_PROFILE_BUTTON_TEXT


async def get_query_kb(
    user_id: int,
) -> InlineKeyboardMarkup:
    """Keyboard that asks moderator to verify or reset user's profile"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=VERIFY_BUTTON_TEXT,
                    callback_data=VerifiedCallbackFactory(user_id=user_id).pack(),
                ),
                InlineKeyboardButton(
                    text=RESET_PROFILE_BUTTON_TEXT,
                    callback_data=ResetProfileCallbackFactory(user_id=user_id).pack(),
                ),
            ]
        ]
    )


VERIFIED_KB = DummyInlineKeyboard(VERIFY_BUTTON_TEXT)

RESET_PROFILE_KB = DummyInlineKeyboard(RESET_PROFILE_BUTTON_TEXT)
