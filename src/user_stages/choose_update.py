"""User chooses which stage to update"""
from fork_stage import produce_fork_stage


ChooseUpdateStage = produce_fork_stage(
    stage_name_arg="Выбрать, какую стадию обновить",
    question_text_arg="Какой пункт обновить?",
)
