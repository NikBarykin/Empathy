from typing import List, Type

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from stage import Stage

from utils.id import get_id
from utils.prev_stage import (
    send_prev_stage_keyboard,
    make_prev_stage_processor,
    PREV_STAGE_FILTER,
)

from .base import ForkStageBase
from .alternatives_keyboard import get_keyboard_for_alternatives


def produce_fork_stage(
    stage_name_arg: str,
    question_text_arg: str,
) -> Type[ForkStageBase]:
    """Fancy function to produce fork-stages with comfort"""
    class ForkStage(ForkStageBase):
        name: str = stage_name_arg
        question_text: str= question_text_arg
        alternatives: List[Type[Stage]] = []

        __main_state = State(state="main_" + name)
        __prepare_state = State(state="prepare_" + name)

        @staticmethod
        async def add_alternative(alternative: Type[Stage]) -> None:
            ForkStage.alternatives.append(alternative)

        @staticmethod
        async def prepare(state: FSMContext):
            await state.set_state(ForkStage.__prepare_state)

            user_id: int = await get_id(state)

            if ForkStage.prev_stage is not None:
                await send_prev_stage_keyboard(user_id)

            result = await Stage.bot.send_message(
                chat_id=user_id,
                text=ForkStage.question_text,
                reply_markup=get_keyboard_for_alternatives(ForkStage.alternatives),
            )

            await state.set_state(ForkStage.__main_state)

            return result

        @staticmethod
        def register(router: Router) -> None:
            """Register ForkStage-processors"""
            if ForkStage.prev_stage is not None:
                router.message.register(
                    make_prev_stage_processor(ForkStage),
                    ForkStage.__main_state,
                    PREV_STAGE_FILTER,
                )

            for stage in ForkStage.alternatives:
                router.callback_query.register(
                    ForkStage.make_processor(stage),
                    ForkStage.__main_state,
                    F.data==stage.name,
                )

    return ForkStage
