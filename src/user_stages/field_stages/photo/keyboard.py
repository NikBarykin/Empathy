from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from stage import Stage
from utils.id import get_id

from .constants import ADD_PROFILE_PHOTO_TEXT


async def has_profile_photo(state: FSMContext) -> bool:
    """Check if user has photos in his telegram-profile"""
    photos = (await Stage.bot.get_user_profile_photos(
        await get_id(state), offset=0, limit=1)).photos
    return len(photos) > 0


async def get_kb(state: FSMContext) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
            keyboard=([[KeyboardButton(text=ADD_PROFILE_PHOTO_TEXT)]]
                      if await has_profile_photo(state)
                      else []),
            resize_keyboard=True,
            one_time_keyboard=True,
    )
