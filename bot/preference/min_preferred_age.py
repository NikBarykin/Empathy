from simple_get_stage import produce_simple_get_stage
from age_filter import AgeFilter


MinPreferredAgeStage = produce_simple_get_stage(
    stage_name="минимальный возраст партнера",
    question_text="Укажи минимальный возраст для твоего партнера",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)
