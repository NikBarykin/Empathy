from simple_get_stage import produce_simple_get_stage
from age_filter import AgeFilter
from aiogram.fsm.context import FSMContext


AgeStage = produce_simple_get_stage(
    stage_name="возраст",
    question_text="Сколько тебе лет?",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)
