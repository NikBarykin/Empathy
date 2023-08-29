from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from utils.id import get_id

from .constants import USE_BIO_FROM_TELEGRAM_TEXT
from .filter import BIO_FILTER
from .logic import get_bio_from_telegram


QUESTION_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=USE_BIO_FROM_TELEGRAM_TEXT)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def get_kb(state: FSMContext) -> ReplyKeyboardMarkup | None:
    """Proposes to user bio from telegram account"""
    bio: str = await get_bio_from_telegram(user_id=await get_id(state))
    if bio is not None and await BIO_FILTER(bio):
        return QUESTION_KB
