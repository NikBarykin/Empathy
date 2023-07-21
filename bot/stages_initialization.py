from stage import Stage, StageType
from stage_mapper import init_personal_mapper, init_preference_mapper
from stage_order import order_stages

from typing import List
from aiogram import Bot, Router


def register_stages(router: Router, *stages: StageType) -> None:
    for stage in stages:
        stage.register(router)


def init_stages(
    router: Router,
    start_stage: StageType,
    personal_stages: List[StageType],
    preference_stages: List[StageType],
    register_stage: StageType,
    match_stage: StageType,
    overwrite_stages: List[StageType],
) -> None:
    stage_sequence = (
        [start_stage] + personal_stages + preference_stages + [register_stage, match_stage]
    )
    Stage.register_stage = register_stage

    order_stages(*stage_sequence)
    register_stages(router, *stage_sequence, *overwrite_stages)

    init_personal_mapper(personal_stages)
    init_preference_mapper(preference_stages)
