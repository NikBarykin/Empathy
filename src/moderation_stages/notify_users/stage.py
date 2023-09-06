from stage import Stage

import sqlalchemy as sa

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.methods import SendMessage

from database.user import User

from utils.id import get_id
from utils.execute_method import execute_method
from utils.prev_stage import (
    PREV_STAGE_KB, PREV_STAGE_FILTER)
from utils.keyboard import RowKeyboard
from utils.order import make_stage_jumper
from utils.logger import create_logger

from .constants import (
    QUESTION_TEXT, INSURANCE_TEXT, SUBMIT_TEXT, WRITE_OTHER_MESSAGE_TEXT)
from .logic import notify_users


class NotifyUsersStage(Stage):
    name: str = "Уведомить пользователей"
    __prepare_state = State(state="prepare_" + name)
    __waiting_message_state = State(state="waiting_message_state_" + name)
    __handling_message_state = State(state="handling_message_state" + name)
    __making_sure_state = State(state="making_sure_state" + name)
    __notifying_users_state = State(state="notifying_users_state" + name)
    __logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext) -> Message:
        """Ask moderator which message to user to notify users"""
        await state.set_state(NotifyUsersStage.__prepare_state)

        user_id: int = await get_id(state)

        result: Message = await execute_method(
            SendMessage(
                chat_id=user_id,
                text=QUESTION_TEXT,
                # if there is a 'prev_stage' we add corresponding keyboard to be able to jump there
                reply_markup=NotifyUsersStage.prev_stage and PREV_STAGE_KB,
            )
        )

        await state.set_state(NotifyUsersStage.__waiting_message_state)

        return result

    @staticmethod
    async def process_message(message: Message, state: FSMContext) -> Message:
        """
            Save received message.
            Show it to moderator and ensure that it is a right message.
            Return message with insurance.
        """
        await state.set_state(NotifyUsersStage.__handling_message_state)

        await state.update_data(
            notify_from_chat_id=message.chat.id,
            notify_message_id=message.message_id,
        )

        user_id: int = message.from_user.id

        result: Message = await execute_method(
            SendMessage(
                chat_id=user_id,
                text=INSURANCE_TEXT,
                reply_markup=(
                    RowKeyboard(
                        SUBMIT_TEXT, WRITE_OTHER_MESSAGE_TEXT
                    )
                ),
            ),
            logger=NotifyUsersStage.__logger,
        )

        await state.set_state(NotifyUsersStage.__making_sure_state)

        return result

    @staticmethod
    async def process_submit_message(
        _: Message,
        state: FSMContext,
    ):
        """Returns result of 'prepare'-method of the next stage"""
        await state.set_state(NotifyUsersStage.__notifying_users_state)

        select_stmt = (
            sa.select(User.id)
            .where(~User.blocked_bot)
            .where(~User.frozen)
        )

        async with Stage.async_session() as session:
            target_ids = (await session.execute(select_stmt)).scalars()

        await notify_users(
            user_ids=target_ids,
            from_chat_id=(await state.get_data())['notify_from_chat_id'],
            message_id=(await state.get_data())['notify_message_id'],
            logger=NotifyUsersStage.__logger,
        )

        NotifyUsersStage.__logger.info("Notified user's successfully")

        return await NotifyUsersStage.next_stage.prepare(state)

    @staticmethod
    async def process_write_other_message(_: Message, state: FSMContext) -> Message:
        """Calls NotifyUsersStage.prepare and returns the result"""
        return await NotifyUsersStage.prepare(state)

    @staticmethod
    def register(router: Router) -> None:
        if NotifyUsersStage.prev_stage is not None:
            router.message.register(
                make_stage_jumper(target_stage=NotifyUsersStage.prev_stage),
                NotifyUsersStage.__waiting_message_state,
                PREV_STAGE_FILTER,
            )

        router.message.register(
            NotifyUsersStage.process_message,
            NotifyUsersStage.__waiting_message_state,
        )

        router.message.register(
            NotifyUsersStage.process_submit_message,
            NotifyUsersStage.__making_sure_state,
            F.text==SUBMIT_TEXT,
        )

        router.message.register(
            NotifyUsersStage.process_write_other_message,
            NotifyUsersStage.__making_sure_state,
            F.text==WRITE_OTHER_MESSAGE_TEXT,
        )
