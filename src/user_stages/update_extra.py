"""User updates additional settings"""
from fork_stage.produce import produce_fork_stage


UpdateExtraStage = produce_fork_stage(
    stage_name_arg="🤯Дополнительные настройки🤯",
    question_text_getter_arg="Какой пункт обновить?",
)
