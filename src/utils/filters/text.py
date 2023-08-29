"""Filter messages containing text"""
from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text is not None
