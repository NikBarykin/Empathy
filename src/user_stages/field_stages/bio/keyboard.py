from aiogram.types import ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

from utils.id import get_id
from utils.keyboard import RowKeyboard

from .filter import BioFilter
from .logic import get_bio_from_telegram


async def get_kb(state: FSMContext) -> ReplyKeyboardMarkup | None:
    """Proposes to user bio from telegram account"""
    bio: str = await get_bio_from_telegram(user_id=await get_id(state))
    if bio is not None and BioFilter.valid_bio(bio):
        return RowKeyboard(bio)
