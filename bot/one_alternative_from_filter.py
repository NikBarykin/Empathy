from typing import Tuple
from aiogram.filters import BaseFilter
from aiogram.types import Message


# TODO: case ignore option
class OneAlternativeFromFilter(BaseFilter):
    def __init__(self, alternatives: Tuple[str]):
        self.alternatives = alternatives

    async def __call__(self, message: Message) -> bool:
        return (message.text is not None
                and message.text.lower() in self.alternatives)
