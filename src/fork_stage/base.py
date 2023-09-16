from logging import Logger
from typing import List, Type, Callable, Awaitable

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageReplyMarkup

from utils.execute_method import execute_method

from stage import Stage

from .alternatives_keyboard import get_keyboard_for_chosen_alternative


class ForkStageBase(Stage):
    """
        Stage that is used to choose one of alternative-stages.
        Alternatives are displayed as inline-buttons attached to one message.

    """
    question_text_getter: str | Callable[[int], Awaitable[str]]
    """question-text or coroutine that builds question-text by user-id"""
    prev_stage_button_text: str
    """Text for a button that jumps to previous-stage"""
    question_photo_getter: None | str | Callable[[int], Awaitable[str]]
    """None or question_photo or coroutine that builds question-photo user-id"""
    description: str
    """Stage-description"""

    alternatives: List[Type[Stage]]
    """Stage-alternatives"""

    @staticmethod
    def add_alternative(alternative: Type[Stage]) -> None:
        """
            Add new alternative
            (should be implemented in derived classes)
        """

    @staticmethod
    def make_processor(destination_stage: Type[Stage], logger: Logger | None = None):
        """Create a processor that prepares chosen alternative-stage"""
        async def process_go_stage(callback: CallbackQuery, state: FSMContext):
            result = await destination_stage.prepare(state)
            # leave only chosen alternative's name in keyboard
            await execute_method(
                EditMessageReplyMarkup(
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.message_id,
                    reply_markup=get_keyboard_for_chosen_alternative(destination_stage),
                ),
                logger=logger
            )
            await callback.answer()
            return result
        return process_go_stage
