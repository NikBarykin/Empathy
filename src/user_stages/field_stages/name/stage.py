from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import raw_getter

from .keyboard import get_kb
from .filter import NameFilter


make_name_stage = FieldStageMaker(
    field_name_arg="name",
    prepare_text_arg="Как тебя зовут?",
    value_getter_arg=raw_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=get_kb,
    invalid_value_text_arg="Имя должно состоять из букв, символа '-' и пробела",
    filter_arg=NameFilter(),
)
