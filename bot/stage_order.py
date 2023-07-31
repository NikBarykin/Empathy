import logging
from get_id import get_id
from stage_mapper import personal_mapper, preference_mapper
from stage import StageType, Stage
from accomplishment_manager import AccomplishmentManager
from aiogram.fsm.context import FSMContext


def order_stages(*stages: StageType):
    global stage_order
    stage_order = stages


async def __get_first_not_completed(state: FSMContext) -> StageType:
    for stage in stage_order:
        if not await AccomplishmentManager.completed(stage, state):
            return stage

    raise RuntimeError(
        "All stages are completed but uncompleted stage was required")


async def prepare_stage_and_state(
    stage: StageType,
    state: FSMContext,
) -> None:
    # order matters: in prepare we can call 'next_stage' again
    await state.set_state(stage.state)
    await stage.prepare(state)


async def next_stage(
        stage: StageType,
        state: FSMContext,
) -> None:
    # order of the following two strings is important
    await AccomplishmentManager.mark_completed(stage, state)
    target_stage: StageType = await __get_first_not_completed(state)
    await prepare_stage_and_state(target_stage, state)
    logging.info(f"current state for user {await get_id(state)} is {target_stage.state}")


async def skip_form(state: FSMContext) -> None:
    stages_to_skip = []
    for mapper in [personal_mapper, preference_mapper]:
        stages_to_skip += [stage for stage in mapper.values()]

    for stage in stages_to_skip:
        await AccomplishmentManager.mark_completed(stage, state)
