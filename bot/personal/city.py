from simple_get_stage import produce_simple_get_stage
from one_alternative_from_filter import OneAlternativeFromFilter
from constants import CITIES


CityStage = produce_simple_get_stage(
    stage_name="город",
    question_text="Твой город? (слитно, например: НижнийНовгород)",
    invalid_value_text="Я не знаю такого города",
    data_update_value_getter=lambda message: message.text.lower(),
    message_filter=OneAlternativeFromFilter(CITIES),
)
