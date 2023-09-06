from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import int_getter

from .constants import QUESTION_TEXT, INVALID_VALUE_TEXT
from .filter import AgeFilter


make_age_stage = FieldStageMaker(
    field_name_arg="age",
    prepare_text_arg=QUESTION_TEXT,
    value_getter_arg=int_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=None,
    invalid_value_text_arg=INVALID_VALUE_TEXT,
    message_filter_arg=AgeFilter(),
)
