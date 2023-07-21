from stage import Stage, StageType
from stage_order import prepare_stage_and_state
from command_start import get_id
from one_alternative_from_filter import OneAlternativeFromFilter

# aiogram
from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext

from .personal import OverwritePersonalStage
from .preference import OverwritePreferenceStage


mapper = {
    OverwritePersonalStage.name: OverwritePersonalStage,
    OverwritePreferenceStage.name: OverwritePreferenceStage,
}


KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=stage_name) for stage_name in mapper.keys()]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
)


class OverwriteStartStage(Stage):
    state = State()
    name: str = "развилка изменений"

    @staticmethod
    async def prepare(
        state: FSMContext,
    ) -> None:
        # TODO: delete prev message
        await Stage.bot.send_message(
            await get_id(state),
            "Какую информацию ты хочешь изменить?",
            reply_markup=KB,
        )

    @staticmethod
    async def process(
        message: Message,
        state: FSMContext,
    ) -> None:
        target_stage: StageType = mapper[message.text]
        await prepare_stage_and_state(target_stage, state)

    @staticmethod
    async def process_invalid_value(
        message: Message,
        state: FSMContext,
    ) -> None:
        await message.reply("Неизвестная опция")

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            OverwriteStartStage.process,
            OneAlternativeFromFilter(mapper.keys()),
            OverwriteStartStage.state,
        )

        router.message.register(
            OverwriteStartStage.process_invalid_value,
            OverwriteStartStage.state,
        )