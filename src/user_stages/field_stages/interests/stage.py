"""User's interests"""
from typing import List, Type

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage, EditMessageText
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from engine.user import update_field, get_field

from stage import Stage
from user_stages.field_stages.base import FieldStageBase

from utils.id import get_id
from utils.keyboard import send_reply_kb
from utils.prev_stage import PREV_STAGE_KB, PREV_STAGE_FILTER
from utils.execute_method import execute_method
from utils.order import make_stage_jumper
from utils.logger import create_logger

from .callback_factory import (
    CheckInterestCallbackFactory, SubmitCallbackFactory)
from .constants import (
    QUESTION_TEXT, SUBMIT_TEXT, MIN_NO_INTERESTS, NOT_ENOUGH_INTERESTS_TEXT)
from .keyboard import get_question_kb, get_submit_kb


def make_interests_stage(stage_name_arg: str) -> Type[Stage]:
    """Create and return interests-stage"""
    class InterestsStage(FieldStageBase):
        """User's interests"""
        name: str = stage_name_arg
        field_name: str = "interests"
        __main_state = State(state="main_" + name)
        __prepare_state = State(state="prepare_" + name)
        __logger = create_logger(name)

        @staticmethod
        async def __get_checked_interests(state: FSMContext) -> List[str]:
            return (await state.get_data())[InterestsStage.field_name]

        @staticmethod
        async def __get_interests_from_db(user_id: int) -> List[str]:
            return await get_field(
                id=user_id, field_name=InterestsStage.field_name)

        @staticmethod
        async def check_field_already_presented(state: FSMContext) -> bool:
            """Defining a method from class-base which is FieldStageBase"""
            user_id = await get_id(state)
            field_value = await InterestsStage.__get_interests_from_db(user_id)
            return field_value is not None

        @staticmethod
        async def prepare(state: FSMContext) -> Message:
            await state.set_state(InterestsStage.__prepare_state)

            user_id: int = await get_id(state)

            checked_interests = (
                await InterestsStage.__get_interests_from_db(user_id) or [])

            await state.update_data(
                **{InterestsStage.field_name: checked_interests})

            if InterestsStage.prev_stage is not None:
                await send_reply_kb(chat_id=user_id, kb=PREV_STAGE_KB)

            result = await execute_method(
                SendMessage(
                    chat_id=user_id,
                    text=QUESTION_TEXT,
                    reply_markup=get_question_kb(checked_interests),
                ),
                logger=InterestsStage.__logger
            )

            await state.set_state(InterestsStage.__main_state)

            return result

        @staticmethod
        async def process_check_interest(
            callback: CallbackQuery,
            callback_data: CheckInterestCallbackFactory,
            state: FSMContext,
        ) -> Message | None:
            """
                Add or remove a user's interest.
                Return new version of question message.
            """
            checked_interests: str = await InterestsStage.__get_checked_interests(state)
            target_interest: str = callback_data.interest

            if target_interest in checked_interests:
                checked_interests.remove(target_interest)
            else:
                checked_interests.append(target_interest)

            result: Message | None = await execute_method(
                EditMessageText(
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.message_id,
                    text=QUESTION_TEXT,
                    reply_markup=get_question_kb(checked_interests),
                ),
                logger=InterestsStage.__logger,
            )

            if result is not None:
                # successfully edited keyboard
                await state.update_data(interests=checked_interests)

            await callback.answer()

            return result

        @staticmethod
        async def process_submit(
            callback: CallbackQuery,
            state: FSMContext,
        ) -> Message:
            """Submit user's interests and go to next stage"""
            checked_interests: str = await InterestsStage.__get_checked_interests(state)

            if len(checked_interests) < MIN_NO_INTERESTS:
                await callback.answer(text=NOT_ENOUGH_INTERESTS_TEXT)
                return

            await update_field(
                id=await get_id(state),
                field_name="interests",
                value=checked_interests,
            )

            await execute_method(
                EditMessageText(
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.message_id,
                    text=SUBMIT_TEXT,
                    reply_markup=get_submit_kb(checked_interests),
                ),
                logger=InterestsStage.__logger

            )

            await callback.answer()

            return await InterestsStage.next_stage.prepare(state)

        @staticmethod
        def register(router: Router) -> None:
            if InterestsStage.prev_stage is not None:
                router.message.register(
                    make_stage_jumper(target_stage=InterestsStage.prev_stage),
                    InterestsStage.__main_state,
                    PREV_STAGE_FILTER,
                )

            router.callback_query.register(
                InterestsStage.process_check_interest,
                CheckInterestCallbackFactory.filter(),
                InterestsStage.__main_state,
            )

            router.callback_query.register(
                InterestsStage.process_submit,
                SubmitCallbackFactory.filter(),
                InterestsStage.__main_state,
            )

    return InterestsStage
