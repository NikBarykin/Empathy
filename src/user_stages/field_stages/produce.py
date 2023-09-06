from typing import Type

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.filters import BaseFilter
from aiogram.methods import SendMessage

from engine.user import update_field, get_field

from stage import Stage

from utils.logger import create_logger
from utils.id import get_id
from utils.keyboard import (
    send_reply_kb, concat_reply_keyboards)
from utils.prev_stage import (
    PREV_STAGE_KB, PREV_STAGE_FILTER)
from utils.execute_method import execute_method
from utils.order import make_stage_jumper

from .base import FieldStageBase


def produce_field_stage(
    stage_name_arg: str,
    field_name_arg: str,
    prepare_text_arg: str,
    value_getter_arg,
    inline_kb_getter_arg,
    reply_kb_getter_arg,
    invalid_value_text_arg: str,
    message_filter_arg: BaseFilter,
) -> Type[Stage]:
    """A trick to produce many stage classes"""
    # TODO: forbid to inherit from this class
    # (there is a problem when a derived class changes next_stage/prev_stage attribute
    # it doesn't change in base [FieldStage] class)
    class FieldStage(FieldStageBase):
        """Basis for a stage that fills some field of user data"""
        name: str = stage_name_arg
        field_name: str = field_name_arg
        inline_kb_getter = inline_kb_getter_arg
        reply_kb_getter = reply_kb_getter_arg
        message_filter = message_filter_arg

        _main_state = State(state="main_" + name)
        _logger = create_logger(stage_name=name)
        _prepare_state = State(state="prepare_" + name)
        _process_state = State(state="process_" + name)

        @staticmethod
        async def _get_reply_kb(state: FSMContext) -> ReplyKeyboardMarkup:
            if FieldStage.reply_kb_getter is None:
                result = None
            elif isinstance(FieldStage.reply_kb_getter, ReplyKeyboardMarkup):
                result = FieldStage.reply_kb_getter
            else:
                result = await FieldStage.reply_kb_getter(state)

            if FieldStage.prev_stage is not None:
                result = concat_reply_keyboards(result, PREV_STAGE_KB)
            return result

        @staticmethod
        async def _get_inline_kb(state: FSMContext) -> InlineKeyboardMarkup:
            if FieldStage.inline_kb_getter is None:
                return None
            elif isinstance(FieldStage.inline_kb_getter, InlineKeyboardMarkup):
                return FieldStage.inline_kb_getter
            else:
                return await FieldStage.inline_kb_getter(state)

        @staticmethod
        async def check_field_already_presented(state: FSMContext) -> bool:
            """User already has this field in database"""
            user_id: int = await get_id(state)
            field_value = await get_field(user_id, FieldStage.field_name)
            return field_value is not None

        @staticmethod
        async def prepare(state: FSMContext):
            """Prepare stage"""
            await state.set_state(FieldStage._prepare_state)

            user_id: int = await get_id(state)

            # If there is no inline-keyboard we can send regular-keyboard
            # with the main message otherwise we have to send it separately
            inline_kb = await FieldStage._get_inline_kb(state)
            reply_kb = await FieldStage._get_reply_kb(state)

            if inline_kb is not None:
                await send_reply_kb(
                    chat_id=user_id,
                    kb=reply_kb,
                )
                main_kb = inline_kb
            else:
                main_kb = reply_kb

            # Send main message
            result = await execute_method(
                SendMessage(
                    chat_id=user_id,
                    text=prepare_text_arg,
                    reply_markup=main_kb,
                )
            )

            await state.set_state(FieldStage._main_state)

            FieldStage._logger.debug(
                "prepared stage for %s", user_id)

            return result

        @staticmethod
        async def _process_set_field(
            message: Message, state: FSMContext
        ) -> Message:
            """
                Process update of user's field and got to next stage.
                Return next-stage's prepare result.
            """
            await state.set_state(FieldStage._process_state)

            await update_field(
                id=await get_id(state),
                field_name=field_name_arg,
                value=await value_getter_arg(message)
            )

            FieldStage._logger.debug(
                "set field for id=%s", await get_id(state))

            return await FieldStage.next_stage.prepare(state)

        @staticmethod
        async def _process_invalid_value(
            message: Message, state: FSMContext
        ):
            """User passed invalid value"""
            await message.answer(invalid_value_text_arg)
            return await FieldStage.prepare(state)

        @staticmethod
        def register(router: Router) -> None:
            """Register handlers"""
            if FieldStage.prev_stage is not None:
                router.message.register(
                    make_stage_jumper(target_stage=FieldStage.prev_stage),
                    FieldStage._main_state,
                    PREV_STAGE_FILTER,
                )

            router.message.register(
                FieldStage._process_set_field,
                FieldStage.message_filter,
                FieldStage._main_state,
            )

            router.message.register(
                FieldStage._process_invalid_value,
                FieldStage._main_state,
            )

    return FieldStage
