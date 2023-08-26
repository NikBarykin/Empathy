from typing import Type
from stages.stage import Stage

from utils.field_base import produce_field_stage
from message_value_getters.text_getters import lower_getter
from filters.choice import ChoiceLowerFilter

from .constants import CITIES


def make_city_stage(stage_name_arg: str) -> Type[Stage]:
    """Create a CityStage"""
    return produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg="city",
        prepare_text_arg="Твой город?",
        value_getter_arg=lower_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=None,
        invalid_value_text_arg="Я не знаю такого города",
        filter_arg=ChoiceLowerFilter(alternatives=CITIES),
    )
