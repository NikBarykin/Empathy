from typing import List, Type

from stage import Stage


class ForkStageBase(Stage):
    """
        Stage that is used to choose one of alternative-stages.
        Alternatives are displayed as inline-buttons attached to one message.

    """
    question_text: str
    """Text of a question message"""
    alternatives: List[Type[Stage]]
    """Stage-alternatives"""

    @staticmethod
    def add_alternative(Type[Stage]) -> None:
        """
            Add new alternative
            (should be implemented in derived classes)
        """
        pass

    @staticmethod
    def make_processor(destination_stage: Type[Stage]):
        """Create a processor that just prepares chosen alternative-stage"""
        async def process_go_stage(callback: CallbackQuery, state: FSMContext):
            result = await destination_stage.prepare(state)
            await callback.answer()
            return result
        return process_go_stage
