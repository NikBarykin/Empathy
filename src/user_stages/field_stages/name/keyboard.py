from aiogram.types import ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from stage import Stage
from utils.id import get_id
from utils.keyboard import RowKeyboard
from .filter import NameFilter


# TODO: move to name-logic or smth alike
async def __get_first_name(user_id: int) -> str | None:
    """Get first name section from user's telegram-account"""
    user_info = await Stage.bot.get_chat(user_id)
    return user_info.first_name


async def get_kb(state: FSMContext) -> ReplyKeyboardMarkup | None:
    """Proposes user's first-name from telegram-account"""
    name = await __get_first_name(user_id=await get_id(state))
    if name is not None and NameFilter.check(name):
        return RowKeyboard(name)
