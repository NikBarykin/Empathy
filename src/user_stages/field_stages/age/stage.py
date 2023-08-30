from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import int_getter

from .constants import MIN_AGE
from .filter import AgeFilter


make_age_stage = FieldStageMaker(
    field_name_arg="age",
    prepare_text_arg="Сколько тебе лет?",
    value_getter_arg=int_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=None,
    invalid_value_text_arg=f"Возраст должен быть числом, не меньше {MIN_AGE}",
    filter_arg=AgeFilter(),
)
