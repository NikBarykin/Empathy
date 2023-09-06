from logging import Logger
from typing import Iterable

from aiogram.methods import CopyMessage

from utils.execute_method import execute_method


async def notify_users(
    user_ids: Iterable[int],
    from_chat_id: int,
    message_id: int,
    logger: Logger | None = None,
) -> None:
    """
        Copy message from chat 'from_chat_id' with id 'message_id' to users with 'user_ids'.
    """
    for user_id in user_ids:
        await execute_method(
            CopyMessage(
                chat_id=user_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
            ),
            logger=logger,
        )
