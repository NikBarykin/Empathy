from logging import Logger

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.methods import EditMessageReplyMarkup, SendMessage

from engine.user import update_field

from stage import Stage

from user_stages.start import StartStage
from user_stages.profile.send import send_profile

from utils.state import get_state_by_id
from utils.logger import create_logger
from utils.prev_stage import PREV_STAGE_FILTER, send_prev_stage_keyboard
from utils.id import get_id
from utils.order import make_stage_jumper
from utils.execute_method import execute_method

from .keyboard import get_query_kb, VERIFIED_KB, RESET_PROFILE_KB
from .constants import (
    RESET_PROFILE_TEXT_FOR_USER, ALL_USERS_VIEWED_TEXT)
from .callback_factory import VerifiedCallbackFactory, ResetProfileCallbackFactory
from .logic import get_unverified_user_id


class VerificationStage(Stage):
    """
        Stage in which moderators verify or reset user's profiles.
        (It is similar to Moderate-Stage but simpler).
    """
    name: str = "верификация пользователей"
    __prepare_state = State(state="prepare_" + name)
    __verification_state = State(state="verification_" + name)
    __logger: Logger = create_logger(name)

    @staticmethod
    async def __process_all_users_viewed(state: FSMContext) -> Message:
        # all user's are viewed
        await execute_method(
            SendMessage(
                chat_id=await get_id(state),
                text=ALL_USERS_VIEWED_TEXT,
            ),
            logger=VerificationStage.__logger,
        )
        return await VerificationStage.next_stage.prepare(state)

    @staticmethod
    async def prepare(state: FSMContext) -> Message:
        "Get next unverified user and send his profile to moderator"""
        await state.set_state(VerificationStage.__prepare_state)

        user_id: int | None = await get_unverified_user_id()

        moderator_id: int = await get_id(state)

        if user_id is None:
            return await VerificationStage.__process_all_users_viewed(state)

        if VerificationStage.prev_stage is not None:
            await send_prev_stage_keyboard(moderator_id)

        profile_msg: Message | None = await send_profile(
            chat_id=moderator_id,
            user_id=user_id,
            reply_markup=await get_query_kb(user_id=user_id),
            logger=VerificationStage.__logger,
        )

        await state.set_state(VerificationStage.__verification_state)

        VerificationStage.__logger.info(
            "Moderator %s is now verifying user %s",
            moderator_id, user_id,
        )

        return profile_msg

    @staticmethod
    async def process_verify(
        callback: CallbackQuery,
        callback_data: VerifiedCallbackFactory,
        state: FSMContext,
    ) -> Message:
        """Verify user (set corresponding field to True)"""
        user_id: int = callback_data.user_id

        await update_field(
            id=user_id,
            field_name="verified",
            value=True,
        )

        moderator_id: int = await get_id(state)

        VerificationStage.__logger.info(
            "moderator %s verified user %s",
            moderator_id, user_id,
        )

        await execute_method(
            EditMessageReplyMarkup(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=VERIFIED_KB,
            ),
            logger=VerificationStage.__logger,
        )

        await callback.answer()
        return await VerificationStage.prepare(state)

    @staticmethod
    async def process_reset_profile(
        callback: CallbackQuery,
        callback_data: VerifiedCallbackFactory,
        state: FSMContext,
    ) -> Message:
        """Reset user's profile"""
        user_id: int = callback_data.user_id

        await execute_method(
            SendMessage(
                chat_id=user_id,
                text=RESET_PROFILE_TEXT_FOR_USER,
            ),
            logger=VerificationStage.__logger,
        )

        await StartStage.prepare(
            state=get_state_by_id(user_id),
            user_id=user_id,
            reset_user=True,
        )

        moderator_id: int = await get_id(state)

        VerificationStage.__logger.info(
            "moderator %s reset profile of user %s",
            moderator_id, user_id,
        )

        await execute_method(
            EditMessageReplyMarkup(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=RESET_PROFILE_KB,
            ),
            logger=VerificationStage.__logger,
        )

        await callback.answer()
        return await VerificationStage.prepare(state)

    @staticmethod
    def register(router: Router) -> None:
        """Register verify/reset profile processors and prev-stage-jumper"""
        if VerificationStage.prev_stage is not None:
            router.message.register(
                make_stage_jumper(target_stage=VerificationStage.prev_stage),
                VerificationStage.__verification_state,
                PREV_STAGE_FILTER,
            )

        router.callback_query.register(
            VerificationStage.process_verify,
            VerifiedCallbackFactory.filter(),
            VerificationStage.__verification_state,
        )

        router.callback_query.register(
            VerificationStage.process_reset_profile,
            ResetProfileCallbackFactory.filter(),
            VerificationStage.__verification_state,
        )
