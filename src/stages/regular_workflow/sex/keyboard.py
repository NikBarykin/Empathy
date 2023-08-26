from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from .constants import SEXES


async def get_kb(_: FSMContext) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=sex) for sex in SEXES]
    ]
    return ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            )
