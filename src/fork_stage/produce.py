from typing import List, Type

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.methods import SendPhoto, SendMessage

from stage import Stage

from utils.id import get_id
from utils.keyboard import RowKeyboard, send_reply_kb
from utils.order import make_stage_jumper
from utils.execute_method import execute_method
from utils.prev_stage import PREV_STAGE_TEXT

from .base import ForkStageBase
from .alternatives_keyboard import get_keyboard_for_alternatives


def produce_fork_stage(
    stage_name_arg: str,
    question_text_getter_arg,
    prev_stage_button_text_arg: str=PREV_STAGE_TEXT,
    question_photo_getter_arg=None,
    description_arg: str="",
) -> Type[ForkStageBase]:
    """Fancy function to produce fork-stages with comfort"""
    class ForkStage(ForkStageBase):
        name: str = stage_name_arg
        question_text_getter = question_text_getter_arg
        prev_stage_button_text = prev_stage_button_text_arg
        question_photo_getter = question_photo_getter_arg
        description: str = description_arg
        alternatives: List[Type[Stage]] = []

        __main_state = State(state="main_" + name)
        __prepare_state = State(state="prepare_" + name)

        @staticmethod
        def add_alternative(alternative: Type[Stage]) -> None:
            ForkStage.alternatives.append(alternative)

        @staticmethod
        async def get_question_text(user_id: int) -> str:
            if isinstance(ForkStage.question_text_getter, str):
                return ForkStage.question_text_getter
            return await ForkStage.question_text_getter(user_id)

        @staticmethod
        async def get_question_photo(user_id: int) -> None | str:
            """Get question-photo using 'user_id' and ForkStage.question_photo_getter"""
            if ForkStage.question_photo_getter is None:
                return None
            elif isinstance(ForkStage.question_photo_getter, str):
                return ForkStage.question_photo_getter
            return await ForkStage.question_photo_getter(user_id)

        @staticmethod
        async def _create_method(user_id: int) -> SendPhoto | SendMessage:
            """
                Create telegram-api-method to be executed.
                Return SendPhoto if there is a question_photo and SendMessage otherwise.
            """
            question_text: str = await ForkStage.get_question_text(user_id)
            question_photo: str | None = await ForkStage.get_question_photo(user_id)
            reply_markup = get_keyboard_for_alternatives(ForkStage.alternatives)

            if question_photo is not None:
                return SendPhoto(
                    chat_id=user_id,
                    photo=question_photo,
                    caption=question_text,
                    reply_markup=reply_markup,
                )
            else:
                return SendMessage(
                    chat_id=user_id,
                    text=question_text,
                    reply_markup=reply_markup,
                )

        @staticmethod
        async def prepare(state: FSMContext) -> Message:
            """Send a question-message with alternatives"""
            await state.set_state(ForkStage.__prepare_state)

            user_id: int = await get_id(state)

            if ForkStage.prev_stage is not None:
                # send prev-stage kb
                await send_reply_kb(
                    chat_id=user_id,
                    kb=RowKeyboard(ForkStage.prev_stage_button_text),
                )

            # create telegram-method
            method = await ForkStage._create_method(user_id)

            # execute method
            result = await execute_method(method)

            await state.set_state(ForkStage.__main_state)

            return result

        @staticmethod
        def register(router: Router) -> None:
            """Register ForkStage-processors"""
            if ForkStage.prev_stage is not None:
                router.message.register(
                    make_stage_jumper(target_stage=ForkStage.prev_stage),
                    ForkStage.__main_state,
                    F.text==ForkStage.prev_stage_button_text,
                )

            for stage in ForkStage.alternatives:
                router.callback_query.register(
                    ForkStage.make_processor(stage),
                    ForkStage.__main_state,
                    F.data==stage.name,
                )

    return ForkStage
