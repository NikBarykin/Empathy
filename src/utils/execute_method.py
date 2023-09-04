"""
    Execute telegram-method by bot.
    Correctly handles situation when user blocked a bot
"""
from logging import Logger

from aiogram.types import Message
from aiogram.methods.base import TelegramMethod
from aiogram.exceptions import TelegramForbiddenError

from stage import Stage

from engine.user import update_field


async def execute_method(
    method: TelegramMethod[Message],
    logger: Logger | None = None,
) -> Message | None:
    """Returns None if something went wrong"""
    try:
        return await Stage.bot(method)
    except TelegramForbiddenError as e:
        # user blocked a bot
        user_id = method.chat_id
        await update_field(
            id=user_id,
            field_name="blocked_bot",
            value=True,
        )
        if logger is not None:
            logger.info("User %s blocked a bot: %s", user_id, e)
    except Exception as e:
        # unexpected exception
        if logger is not None:
            logger.error(
                "Unexpected error during method %s execution: %s", method, e)
