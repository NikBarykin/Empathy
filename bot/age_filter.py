from aiogram.types import Message
from aiogram.filters import BaseFilter


class AgeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.text is not None
            and
            message.text.isnumeric()
            and
            18 <= int(message.text) <= 99
        )
