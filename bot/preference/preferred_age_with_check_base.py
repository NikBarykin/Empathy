from stage import StageType
from preference.min_preferred_age_simple import MinPreferredAgeSimpleStage
from preference.max_preferred_age_simple import MaxPreferredAgeSimpleStage

from aiogram.fsm.context import FSMContext

from typing import Optional


def produce_preffered_age_with_check(base_age_stage: StageType):
    class PreferredAgeStageWithCheckBase(base_age_stage):
        @staticmethod
        async def check_min_not_greater_than_max(state: FSMContext):
            min_preferred_age: Optional[int] = (
                (await state.get_data())
                .get(MinPreferredAgeSimpleStage.name, None))

            max_preferred_age: Optional[int] = (
                (await state.get_data())
                .get(MaxPreferredAgeSimpleStage.name, None))

            return (min_preferred_age is None or max_preferred_age is None
                    or min_preferred_age <= max_preferred_age)

        @staticmethod
        async def process(message: Message, state: FSMContext) -> None:
            await base_age_stage.process(message, state)

            if not await check_min_not_greater_than_max(state):
                message.answer
