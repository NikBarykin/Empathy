"""Freeze user's profile"""
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from stages.stage import Stage, go_next_stage

from utils.logger import create_logger
from utils.id import get_id

from .logic import freeze_user, unfreeze_user

from .constants import (
    SUCCESS_FREEZE_TEXT,
    SUCCESS_UNFREEZE_TEXT,
    QUERY_UNFREEZE_TEXT,
)
from .keyboard import QUERY_KB


class FreezeStage(Stage):
    name: str = "freeze-stage"
    __main_state = State()
    __prepare_state = State("prepare")
    __logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext):
        await state.set_state(FreezeStage.__prepare_state)

        user_id: int = await get_id(state)
        await freeze_user(user_id, logger=FreezeStage.__logger)

        result = await Stage.bot.send_message(
            chat_id=user_id,
            text=SUCCESS_FREEZE_TEXT,
            reply_markup=QUERY_KB,
        )

        await state.set_state(FreezeStage.__main_state)
        return result

    @staticmethod
    async def process_unfreeze(message: Message, state: FSMContext):
        """Unfreeze user's profile"""
        user_id: int = await get_id(state)
        await unfreeze_user(user_id, logger=FreezeStage.__logger)
        await message.answer(text=SUCCESS_UNFREEZE_TEXT)
        return go_next_stage(
            departure=FreezeStage, state=state)

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            FreezeStage.process_unfreeze,
            FreezeStage.__main_state,
            F.text==QUERY_UNFREEZE_TEXT,
        )
