from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import raw_getter

from .keyboard import get_kb
from .filter import NameFilter

from .constants import QUESTION_TEXT, INVALID_VALUE_TEXT


make_name_stage = FieldStageMaker(
    field_name_arg="name",
    prepare_text_arg=QUESTION_TEXT,
    value_getter_arg=raw_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=get_kb,
    invalid_value_text_arg=INVALID_VALUE_TEXT,
    message_filter_arg=NameFilter(),
)
