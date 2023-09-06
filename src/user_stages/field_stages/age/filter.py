"""Filter for user's age"""

from aiogram.filters import BaseFilter
from aiogram.types import Message

from .constants import MIN_AGE, MAX_AGE


class AgeFilter(BaseFilter):
    """Check user's message that is meant to contain user's age"""
    async def __call__(self, message: Message) -> bool:
        return (
            message.text
            and
            message.text.isnumeric()
            and
            MIN_AGE <= int(message.text) <= MAX_AGE
        )
