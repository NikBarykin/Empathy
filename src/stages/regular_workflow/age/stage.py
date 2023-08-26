from typing import Type
from stages.stage import Stage

from utils.field_base import produce_field_stage
from message_value_getters.text_getters import int_getter

from .constants import MIN_AGE
from .filter import AgeFilter


def make_age_stage(stage_name_arg: str) -> Type[Stage]:
    """Create a AgeStage"""
    return produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg="age",
        prepare_text_arg="Сколько тебе лет?",
        value_getter_arg=int_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=None,
        invalid_value_text_arg=f"Возраст должен быть числом, не меньше {MIN_AGE}",
        filter_arg=AgeFilter(),
    )
