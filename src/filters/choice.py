"""Choose one alternative from given ones"""

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChoiceLowerFilter(BaseFilter):
    def __init__(self, alternatives):
        self.alternatives = alternatives

    async def __call__(self, message: Message) -> bool:
        return message.text and message.text.lower() in self.alternatives
