"""User chooses which stage to update"""
from fork_stage.produce import produce_fork_stage


UpdateProfileStage = produce_fork_stage(
    stage_name_arg="🎁Обновить анкету🎁",
    question_text_getter_arg="Какой пункт обновить?",
)
