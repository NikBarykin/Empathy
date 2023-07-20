from .base import OverwriteStageBase
from stage import Stage

from stage_mapper import personal_mapper, StageMapper

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


class OverwritePersonalStage(OverwriteStageBase):
    state = State()

    @staticmethod
    def get_state():
        return OverwritePersonalStage.state

    @staticmethod
    def get_stage_mapper() -> StageMapper
        return personal_mapper
