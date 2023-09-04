"""Send user's profile to some chat"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.methods import SendPhoto

from utils.execute_method import execute_method

from .logic import get_profile_caption, get_profile_photo


async def make_send_profile_method(
    chat_id: int,
    user_id: int,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> SendPhoto:
    return SendPhoto(
            chat_id=chat_id,
            photo=await get_profile_photo(user_id),
            caption=await get_profile_caption(user_id),
            reply_markup=reply_markup,
        )


async def send_profile(
    chat_id: int,
    user_id: int,
    reply_markup: InlineKeyboardMarkup | None = None,
):
    """Send profile of 'user_id' to 'chat_id' and attach 'reply_markup' to it"""
    return await execute_method(
        await make_send_profile_method(chat_id, user_id, reply_markup))
