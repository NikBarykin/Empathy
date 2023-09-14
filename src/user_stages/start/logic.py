from aiogram.types import Chat
from aiogram.methods import GetChat

from utils.execute_method import execute_method


async def user_has_private_forwards(user_id: int) -> bool | None:
    """
        Check if user has private forwards
        (which means that his messages can not be forwarded
        and bot can't send a link to his profile when match happens).
        Return None if something unexpected happened.
    """
    chat: Chat | None = await execute_method(
        # private chat
        GetChat(chat_id=user_id)
    )
    if chat is None:
        return chat
    return chat.has_private_forwards
