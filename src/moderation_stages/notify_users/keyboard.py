from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.keyboard import make_row_reply_keyboard

from .constants import SUBMIT_TEXT, WRITE_OTHER_MESSAGE_TEXT


INSURANCE_KB = make_row_reply_keyboard(SUBMIT_TEXT, WRITE_OTHER_MESSAGE_TEXT)
