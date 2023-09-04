from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import lower_getter
from utils.filters.choice import ChoiceLowerFilter

from .constants import SEXES
from .keyboard import get_kb


make_sex_stage = FieldStageMaker(
    field_name_arg="sex",
    prepare_text_arg="Твой пол?",
    value_getter_arg=lower_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=get_kb,
    invalid_value_text_arg=f"Допустимые значения: {SEXES}",
    message_filter_arg=ChoiceLowerFilter(alternatives=SEXES),
)
