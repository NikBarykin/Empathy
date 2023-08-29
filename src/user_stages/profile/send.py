"""Send user's profile to some chat"""
from aiogram.types import InlineKeyboardMarkup

from stage import Stage
from database.user import User
from .constants import get_profile_caption


async def send_profile(
    chat_id: int,
    user: User,
    reply_markup: InlineKeyboardMarkup | None = None,
):
    # TODO: process exception
    await Stage.bot.send_photo(
        chat_id=chat_id,
        photo=user.photo,
        caption=get_profile_caption(user),
        reply_markup=reply_markup,
    )
