"""Filter messages containing text"""
from aiogram.filters import BaseFilter
from aiogram.types import Message


class BioFilter(BaseFilter):
    @staticmethod
    def valid_bio(bio: str) -> bool:
        return True

    async def __call__(self, message: Message) -> bool:
        return message.text is not None and BioFilter.valid_bio(message.text)
