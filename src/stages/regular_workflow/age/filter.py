"""Filter for user's age"""

from aiogram.filters import BaseFilter
from aiogram.types import Message

from .constants import MIN_AGE


class AgeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.text
            and
            message.text.isnumeric()
            and
            MIN_AGE <= int(message.text)
        )
