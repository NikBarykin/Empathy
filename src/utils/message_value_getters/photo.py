"""Photo getters"""
from aiogram.types import Message


async def first_photo_getter(message: Message):
    """Gets firs photo from presented in message"""
    # -1, because we want the best quality of photo
    return message.photo[-1].file_id
