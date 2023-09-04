from utils.field_stage_maker import FieldStageMaker

from .message_value_getter import get_city_name
from .filter import CityFilter


make_city_stage = FieldStageMaker(
    field_name_arg="city",
    prepare_text_arg="Твой город?",
    value_getter_arg=get_city_name,
    inline_kb_getter_arg=None,
    reply_kb_getter_arg=None,
    invalid_value_text_arg="Я не знаю такого города",
    message_filter_arg=CityFilter(),
)
