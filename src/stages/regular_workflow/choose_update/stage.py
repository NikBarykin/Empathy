"""User chooses which stage to update"""
from typing import Type

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from stages.stage import Stage, go_stage
from utils.id import get_id

from utils.prev_stage import (
    send_prev_stage_keyboard,
    make_prev_stage_processor,
    PREV_STAGE_FILTER,
)

from .constants import (
    TARGET_STAGES,
    QUERY_TEXT,
)
from .keyboard import QUERY_INLINE_KB


class ChooseUpdateStage(Stage):
    __prepare_state = State(state="prepare")
    __main_state = State(state="main")

    @staticmethod
    async def prepare(state: FSMContext):
        await state.set_state(ChooseUpdateStage.__prepare_state)

        user_id: int = await get_id(state)

        result = await Stage.bot.send_message(
            chat_id=user_id,
            text=QUERY_TEXT,
            reply_markup=QUERY_INLINE_KB,
        )

        await send_prev_stage_keyboard(user_id)

        await state.set_state(ChooseUpdateStage.__main_state)

        return result

    @staticmethod
    def make_processor(destination_stage: Type[Stage]):
        async def process_go_stage(callback: CallbackQuery, state: FSMContext):
            result = await go_stage(
                departure=ChooseUpdateStage,
                destination=destination_stage,
                state=state,
            )
            await callback.answer()
            return result
        return process_go_stage

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            make_prev_stage_processor(ChooseUpdateStage),
            ChooseUpdateStage.__main_state,
            PREV_STAGE_FILTER,
        )

        for stage in TARGET_STAGES:
            router.callback_query.register(
                ChooseUpdateStage.make_processor(stage),
                ChooseUpdateStage.__main_state,
                F.text==stage.name,
            )
