"""User's name filters"""

from aiogram.filters import BaseFilter
from aiogram.types import Message


class NameFilter(BaseFilter):
    @staticmethod
    def check_char(char: str) -> bool:
        """Check single character"""
        return (
            char.isalpha()
            or
            char.isspace()
            or
            char == '-'
        )

    @staticmethod
    def check(name: str) -> bool:
        """Check username"""
        return (
            len(name) <= 64
            and
            all(map(NameFilter.check_char, name))
        )

    async def __call__(self, message: Message) -> bool:
        return message.text and NameFilter.check(message.text)