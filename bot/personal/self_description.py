from simple_get_stage import produce_simple_get_stage
from aiogram import F
from db.config import SELF_DESCRIPTION_MAX_LEN


SelfDescriptionStage = produce_simple_get_stage(
    stage_name="о себе",
    question_text=f"Напиши немного о себе в свободной форме (не более {SELF_DESCRIPTION_MAX_LEN} символов)",
    data_update_value_getter=lambda message: message.text,
    message_filter=F.text.len() <= SELF_DESCRIPTION_MAX_LEN,
    invalid_value_text=f"Некорректное описание (длина должна быть не более {SELF_DESCRIPTION_MAX_LEN} символов)",
)
