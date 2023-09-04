from typing import Callable, Awaitable, Any
from aiogram.types import (
    Message, InlineKeyboardMarkup, ReplyKeyboardMarkup)
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from stage import Stage


class FieldStageBase(Stage):
    """
        Stage that corresponds to one of user's specific fields.
        When user go through this stage, he fills that field.
    """
    # TODO: attribute-comments
    field_name: str
    prepare_text: str
    # TODO: rename
    value_getter: Callable[[Message], Awaitable[Any]]
    inline_kb_getter: None | Callable[[FSMContext], Awaitable[InlineKeyboardMarkup]]
    reply_kb_getter: None | Callable[[FSMContext], Awaitable[ReplyKeyboardMarkup]]
    invalid_value_text: str
    message_filter: BaseFilter

    @staticmethod
    async def check_field_already_presented(state: FSMContext) -> bool:
        """Check whether field 'field_name' is already filled in database"""
