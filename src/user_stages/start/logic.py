from typing import Type

from aiogram.fsm.context import FSMContext

from user_stages.config.declarations.forward_stages import FORWARD_STAGES

from field_stage import FieldStageBase


async def get_last_completed_stage(state: FSMContext) -> Type[FieldStageBase] | None:
    """
        Find the last stage from forward-stages that should be skipped
        (because they are already completed)
    """
    for i in range len(FORWARD_STAGES):
        if not await FORWARD_STAGES[i].check_field_already_presented(state):

            return None


    for


    i = 0
    while i < len(FORWARD_STAGES):
        if FORWARD_STAGES[i]
