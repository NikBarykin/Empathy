from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import int_getter

from .constants import INVALID_VALUE_TEXT
from .filter import AgeFilter


make_min_partner_age_stage = FieldStageMaker(
    field_name_arg="min_partner_age",
    prepare_text_arg="Минимальный возраст твоего партнера",
    value_getter_arg=int_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=None,
    invalid_value_text_arg=INVALID_VALUE_TEXT,
    message_filter_arg=AgeFilter(),
)


make_max_partner_age_stage = FieldStageMaker(
    field_name_arg="max_partner_age",
    prepare_text_arg="Максимальный возраст твоего партнера",
    value_getter_arg=int_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=None,
    invalid_value_text_arg=INVALID_VALUE_TEXT,
    message_filter_arg=AgeFilter(),
)
