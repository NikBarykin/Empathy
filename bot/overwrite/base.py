import logging

from stage import Stage, StageType
from stage_order import prepare_stage_and_state
from command_start import get_id
from one_alternative_from_filter import OneAlternativeFromFilter
from accomplishment_manager import AccomplishmentManager
from stage_mapper import StageMapper

from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext


def produce_overwrite_stage(
    stage_name: str,
    mapper: StageMapper,
) -> StageType:
    def get_kb():
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=stage_name)] for stage_name in mapper.keys()
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return kb

    class OverwriteStageBase(Stage):
        state = State(state=stage_name)
        name: str = stage_name

        @staticmethod
        async def prepare(state: FSMContext):
            await Stage.bot.send_message(
                await get_id(state),
                "Выбери конкретную стадию",
                reply_markup=get_kb(),
            )

        @staticmethod
        async def process(
            message: Message,
            state: FSMContext,
        ) -> None:
            target_stage: StageType = mapper[message.text.lower()]

            await AccomplishmentManager.mark_uncompleted(target_stage, state)
            await AccomplishmentManager.mark_uncompleted(
                Stage.register_stage, state)

            logging.info(f"target_stage: {target_stage.name} is being overwritten")

            await prepare_stage_and_state(target_stage, state)

        @staticmethod
        async def process_invalid_value(message: Message) -> None:
            message.answer("Неизвестная позиция")

        @staticmethod
        def register(router: Router):
            router.message.register(
                OverwriteStageBase.process,
                OneAlternativeFromFilter(mapper.keys()),
                OverwriteStageBase.state,
            )

            router.message.register(
                OverwriteStageBase.process_invalid_value,
                OverwriteStageBase.state,
            )
    return OverwriteStageBase
