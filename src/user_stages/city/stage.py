from utils.field_stage_maker import FieldStageMaker
from utils.message_value_getters.text import lower_getter
from utils.filters.choice import ChoiceLowerFilter

from .constants import CITIES


make_city_stage = FieldStageMaker(
    field_name_arg="city",
    prepare_text_arg="Твой город?",
    value_getter_arg=lower_getter,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=None,
    invalid_value_text_arg="Я не знаю такого города",
    filter_arg=ChoiceLowerFilter(alternatives=CITIES),
)
