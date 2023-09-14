from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from stage import Stage


def get_state_by_id(user_id: int) -> FSMContext:
    """get user's aiogram-state by his id"""
    return FSMContext(
        storage=Stage.dp.storage,
        key=StorageKey(
            # all chats are private
            chat_id=user_id,
            user_id=user_id,
            bot_id=Stage.bot.id)
    )
