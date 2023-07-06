from matching.rating_callback_factory import RatingCallbackFactory

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

from constants import (
        LIKE_EMOJI,
        DISLIKE_EMOJI,
        )


def get_inline_kb(
        subj_telegram_id: int,
        obj_telegram_id: int,
        ) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
            text=LIKE_EMOJI,
            callback_data=RatingCallbackFactory(
                liked=True,
                subj_telegram_id=subj_telegram_id,
                obj_telegram_id=obj_telegram_id,
                )
            )

    builder.button(
            text=DISLIKE_EMOJI,
            callback_data=RatingCallbackFactory(
                liked=False,
                subj_telegram_id=subj_telegram_id,
                obj_telegram_id=obj_telegram_id,
                )
            )

    builder.adjust(2)

    return builder.as_markup()


def get_reply_kb() -> ReplyKeyboardMarkup:
    buttons = [[types.KeyboardButton(text="match")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
