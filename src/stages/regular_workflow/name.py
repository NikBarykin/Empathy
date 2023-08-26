from stages.stage import Stage
from utils.field_base import produce_field_stage

from keyboards.name import get_kb

from filters.name import NameFilter

from message_value_getters.text_getters import raw_getter


def make_name_stage(stage_name_arg: str):
    """Create a NameStage"""
    return produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg="name",
        prepare_text_arg="Как тебя зовут?",
        value_getter_arg=raw_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=get_kb,
        invalid_value_text_arg="Имя должно состоять из букв, символа '-' и пробела",
        filter_arg=NameFilter(),
    )
