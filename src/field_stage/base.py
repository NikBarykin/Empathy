from stage import Stage
from aiogram.fsm.context import FSMContext


class FieldStageBase(Stage):
    """
        Stage that corresponds to one of user's specific fields.
        When user go through this stage, he fills that field.
    """
    field_name: str = None

    @staticmethod
    async def check_field_already_presented(state: FSMContext) -> bool:
        """Check whether field 'field_name' is already filled in database"""
