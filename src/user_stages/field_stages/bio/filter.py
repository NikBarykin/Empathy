"""Filter messages containing text"""
from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.user import MAX_BIO_SZ


class BioFilter(BaseFilter):
    @staticmethod
    def valid_bio(bio: str) -> bool:
        return len(bio) <= MAX_BIO_SZ

    async def __call__(self, message: Message) -> bool:
        return message.text is not None and BioFilter.valid_bio(message.text)
