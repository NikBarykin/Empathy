from stage import Stage
from aiogram.fsm.context import FSMContext
from stage_order import next_stage


class IdStage(Stage):
    name: str = "id пользователя"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await state.update_data(**{IdStage.name: message})
        await next_stage(IdStage, state)


async def get_id(state: FSMContext) ->
