"""Keyboards for freeze-stage"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .constants import QUERY_UNFREEZE_TEXT


QUERY_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=QUERY_UNFREEZE_TEXT)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
