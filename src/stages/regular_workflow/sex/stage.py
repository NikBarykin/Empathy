from typing import Type
from stages.stage import Stage

from utils.field_base import produce_field_stage
from message_value_getters.text_getters import lower_getter
from filters.choice import ChoiceLowerFilter

from .constants import SEXES
from .keyboard import get_kb


def make_sex_stage(stage_name_arg: str) -> Type[Stage]:
    """Create a SexStage"""
    return produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg="sex",
        prepare_text_arg="Твой пол?",
        value_getter_arg=lower_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=get_kb,
        invalid_value_text_arg=f"Допустимые значения: {SEXES}",
        filter_arg=ChoiceLowerFilter(alternatives=SEXES),
    )
