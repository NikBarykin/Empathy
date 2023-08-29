from typing import Type

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.filters import BaseFilter

from engine.user import update_field, get_field

from stage import Stage, go_next_stage

from utils.logger import create_logger
from utils.id import get_id
from utils.keyboard import (
    send_reply_kb, concat_reply_keyboards)
from utils.prev_stage import (
    PREV_STAGE_KB, PREV_STAGE_FILTER, make_prev_stage_processor)

from .base import FieldStageBase


def produce_field_stage(
    stage_name_arg: str,
    field_name_arg: str,
    prepare_text_arg: str,
    value_getter_arg,
    inline_kb_getter_arg,
    reply_kb_getter_arg,
    invalid_value_text_arg: str,
    filter_arg: BaseFilter,
) -> Type[Stage]:
    """A trick to produce many stage classes"""
    class FieldStage(FieldStageBase):
        """Basis for a stage that fills some field of user data"""
        name: str = stage_name_arg
        field_name: str = field_name_arg
        _main_state = State(state="main_" + stage_name_arg)
        _logger = create_logger(stage_name=stage_name_arg)
        _prepare_state = State(state="prepare_" + stage_name_arg)
        _process_state = State(state="process_" + stage_name_arg)

        @staticmethod
        async def _get_reply_kb(state: FSMContext) -> ReplyKeyboardMarkup:
            # 'and' in case reply_kb_getter_arg is None
            result = reply_kb_getter_arg and await reply_kb_getter_arg(state)
            if FieldStage.prev_stage is not None:
                result = concat_reply_keyboards(result, PREV_STAGE_KB)
            return result

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
            if inline_kb_getter_arg is not None:
                await send_reply_kb(
                    chat_id=user_id,
                    kb=await FieldStage._get_reply_kb(state),
                )
                main_kb_getter = inline_kb_getter_arg
            else:
                main_kb_getter = FieldStage._get_reply_kb

            # Send main message
            result = await Stage.bot.send_message(
                user_id,
                prepare_text_arg,
                reply_markup=await main_kb_getter(state),
            )

            await state.set_state(FieldStage._main_state)

            FieldStage._logger.debug(
                "prepared stage for %s", user_id)

            return result

        @staticmethod
        async def _process_set_field(
            message: Message, state: FSMContext
        ):
            """Process update of user's field and got to next stage"""
            await state.set_state(FieldStage._process_state)

            await update_field(
                id=await get_id(state),
                field_name=field_name_arg,
                value=await value_getter_arg(message)
            )

            FieldStage._logger.debug(
                "set field for id=%s", await get_id(state))

            return await go_next_stage(departure=FieldStage, state=state)

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
                    make_prev_stage_processor(FieldStage),
                    FieldStage._main_state,
                    PREV_STAGE_FILTER,
                )

            router.message.register(
                FieldStage._process_set_field,
                filter_arg,
                FieldStage._main_state,
            )

            router.message.register(
                FieldStage._process_invalid_value,
                FieldStage._main_state,
            )

    return FieldStage
