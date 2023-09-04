from fork_stage.produce import produce_fork_stage


ActionChoiceStage = produce_fork_stage(
    stage_name_arg="Выбор действия",
    question_text_getter_arg="Выбери действие",
)
