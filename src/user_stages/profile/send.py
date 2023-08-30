"""Send user's profile to some chat"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.methods import SendPhoto

from database.user import User
from utils.execute_method import execute_method

from .constants import get_profile_caption


async def send_profile(
    chat_id: int,
    user: User,
    reply_markup: InlineKeyboardMarkup | None = None,
):
    # TODO: process exception
    return await execute_method(
        SendPhoto(
            chat_id=chat_id,
            photo=user.photo,
            caption=get_profile_caption(user),
            reply_markup=reply_markup,
        )
    )
