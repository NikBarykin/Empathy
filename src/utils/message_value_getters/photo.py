"""Photo getters"""
from aiogram.types import Message


async def first_photo_getter(message: Message):
    """Gets firs photo from presented in message"""
    return message.photo[0].file_id
