"""User's interests"""
from typing import List, Type

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from engine.user import update_field, get_field

from stage import Stage, go_next_stage
from field_stage import FieldStageBase

from utils.id import get_id
from utils.keyboard import send_reply_kb
from utils.prev_stage import PREV_STAGE_KB, make_prev_stage_processor, PREV_STAGE_FILTER

from .callback_factory import (
    CheckInterestCallbackFactory, SubmitCallbackFactory)
from .constants import (
    QUESTION_TEXT, SUBMIT_TEXT, MIN_NO_INTERESTS, NOT_ENOUGH_INTERESTS_TEXT)
from .keyboard import get_question_kb, get_submit_kb


def make_interests_stage(stage_name_arg: str) -> Type[Stage]:
    class InterestsStage(FieldStageBase):
        """User's interests"""
        name: str = stage_name_arg
        field_name: str = "interests"
        __main_state = State(state="main")
        __prepare_state = State(state="prepare")

        @staticmethod
        async def __get_checked_interests(state: FSMContext) -> List[str]:
            return (await state.get_data())[InterestsStage.field_name]

        @staticmethod
        async def __get_interests_from_db(user_id: int) -> List[str]:
            return await get_field(id=user_id, field_name=InterestsStage.field_name)

        @staticmethod
        async def check_field_already_presented(state: FSMContext) -> bool:
            """Defining a method from class-base which is FieldStageBase"""
            user_id = await get_id(state)
            field_value = await InterestsStage.__get_interests_from_db(user_id)
            return field_value is not None

        @staticmethod
        async def prepare(state: FSMContext):
            await state.set_state(InterestsStage.__prepare_state)

            user_id: int = await get_id(state)

            checked_interests = (
                await InterestsStage.__get_interests_from_db(user_id) or [])

            await state.update_data(
                **{InterestsStage.field_name: checked_interests})

            await send_reply_kb(chat_id=user_id, kb=PREV_STAGE_KB)

            result = await Stage.bot.send_message(
                chat_id=user_id,
                text=QUESTION_TEXT,
                reply_markup=get_question_kb(checked_interests),
            )

            await state.set_state(InterestsStage.__main_state)

            return result

        @staticmethod
        async def process_check_interest(
            callback: CallbackQuery,
            callback_data: CheckInterestCallbackFactory,
            state: FSMContext,
        ):
            """Add or remove a user's interest"""
            checked_interests: str = await InterestsStage.__get_checked_interests(state)
            target_interest: str = callback_data.interest

            if target_interest in checked_interests:
                checked_interests.remove(target_interest)
            else:
                checked_interests.append(target_interest)

            await state.update_data(interests=checked_interests)

            # TODO: handle exception (it can throw smt like SAME_MARKUP_ERROR)
            result = await callback.message.edit_text(
                text=QUESTION_TEXT,
                reply_markup=get_question_kb(checked_interests),
            )

            await callback.answer()

            return result

        @staticmethod
        async def process_submit(
            callback: CallbackQuery,
            state: FSMContext,
        ):
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

            await callback.message.edit_text(
                text=SUBMIT_TEXT,
                reply_markup=get_submit_kb(checked_interests),
            )

            await callback.answer()

            return await go_next_stage(departure=InterestsStage, state=state)

        @staticmethod
        def register(router: Router) -> None:
            if InterestsStage.prev_stage is not None:
                router.message.register(
                    make_prev_stage_processor(InterestsStage),
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
