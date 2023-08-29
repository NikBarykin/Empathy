from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .constants import TARGET_STAGES


QUERY_INLINE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=stage.name, callback_data=stage.name)]
        for stage in TARGET_STAGES
    ]
)
