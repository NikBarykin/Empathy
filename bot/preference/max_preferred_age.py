from simple_get_stage import produce_simple_get_stage
from age_filter import AgeFilter


# TODO: process max age less than min age
MaxPreferredAgeStage = produce_simple_get_stage(
    stage_name="максимальный возраст партнера",
    question_text="Укажи максимальный возраст для твоего партнера",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)
