"""Check whether a user is a moderator or not"""
from logging import Logger

from aiogram.filters import BaseFilter
from aiogram.types import Message

from .constants import MODERATORS


class ModeratorFilter(BaseFilter):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def __call__(self, message: Message) -> bool:
        return any(
            moder_id.check_if_message_from_moderator(message, self.logger)
            for moder_id in MODERATORS)
