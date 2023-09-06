from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import lower_getter
from utils.filters.choice import ChoiceLowerFilter
from utils.keyboard import RowKeyboard

from .constants import (
    QUERY_TEXT, INVALID_VALUE_TEXT, RELATIONSHIP_GOALS)


make_relationship_goal_stage = FieldStageMaker(
    field_name_arg="relationship_goal",
    prepare_text_arg=QUERY_TEXT,
    value_getter_arg=lower_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=RowKeyboard(*RELATIONSHIP_GOALS),
    invalid_value_text_arg=INVALID_VALUE_TEXT,
    message_filter_arg=ChoiceLowerFilter(alternatives=RELATIONSHIP_GOALS),
)
