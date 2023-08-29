from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_factory import GoFreezeCallbackFactory, GoUpdateCallbackFactory
from .constants import UPDATE_BUTTON_TEXT, FREEZE_BUTTON_TEXT


QUERY_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text=UPDATE_BUTTON_TEXT, callback_data=GoUpdateCallbackFactory().pack())],
        [InlineKeyboardButton(
            text=FREEZE_BUTTON_TEXT, callback_data=GoFreezeCallbackFactory().pack())]
    ]
)
