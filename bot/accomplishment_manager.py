from stage import StageType
from aiogram.fsm.context import FSMContext


class AccomplishmentManager:
    @staticmethod
    def stage_key(stage: StageType) -> str:
        return stage.name + "_completed"

    @staticmethod
    async def __mark_accomplishment(
        stage: StageType,
        state: FSMContext,
        completed: bool,
    ) -> None:
        await state.update_data(
            **{AccomplishmentManager.stage_key(stage): completed}
        )

    @staticmethod
    async def mark_completed(stage: StageType, state: FSMContext) -> None:
        await AccomplishmentManager.__mark_accomplishment(stage, state, True)

    @staticmethod
    async def mark_uncompleted(stage: StageType, state: FSMContext) -> None:
        await AccomplishmentManager.__mark_accomplishment(stage, state, False)

    @staticmethod
    async def completed(stage: StageType, state: FSMContext) -> bool:
        return (
            (await state.get_data())
            .get(AccomplishmentManager.stage_key(stage), False)
        )
