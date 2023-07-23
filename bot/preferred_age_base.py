from stage import Stage, StageType
from get_id import get_id
from stage_order import next_stage

from aiogram.types import Message
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext


MIN_PREF_AGE_STAGE_NAME = "минимальный возраст партнера"
MAX_PREF_AGE_STAGE_NAME = "максимальный возраст партнера"


def produce_preferred_age_stage(
    stage_name: str,
    question_text: str,
) -> StageType:
    class PreferredAgeStage(Stage):
        name: str = stage_name
        state = State(state=stage_name)

        @staticmethod
        async def prepare(state: FSMContext) -> None:
            Stage.bot.send_message(await get_id(state), text=question_text)

        @staticmethod
        async def check_min_not_greater_than_max(state: FSMContext):
            min_preferred_age: Optional[int] = (
                (await state.get_data())
                .get(MIN_PREF_AGE_STAGE_NAME))

            max_preferred_age: Optional[int] = (
                (await state.get_data())
                .get(MAX_PREF_AGE_STAGE_NAME))

            return (min_preferred_age is None or max_preferred_age is None
                    or min_preferred_age <= max_preferred_age)

        @staticmethod
        async def process(message: Message, state: FSMContext) -> None:
            await state.update_data(
                **{PreferredAgeStage.name: int(message.text)})

            if not PreferredAgeStage.check_min_not_greater_than_max(state):
                await message.reply(
                    "Минимальный возраст не может быть больше максимального")
                return

            await next_stage(PreferredAgeStage, state)

        @staticmethod
        async def process(message: Message, state: FSMContext)

        @staticmethod
