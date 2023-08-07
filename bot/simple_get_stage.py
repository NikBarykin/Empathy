import logging
from get_id import get_id
from stage_order import next_stage
from stage import Stage, StageType

# aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import BaseFilter

from typing import Dict, Any, Awaitable, Callable, Optional


async def get_empty_reply_markup(_: FSMContext) -> None:
    return None


def produce_simple_get_stage(
    stage_name: str,
    field_name, str,
    question_text: str,
    # TODO: better type annotation
    data_update_value_getter: Callable[[Message], Any],
    message_filter: BaseFilter,
    # TODO: maybe it should return Awaitable[Any]
    invalid_value_text: str,
    question_reply_markup_getter: Callable[[FSMContext], Awaitable[Optional[ReplyKeyboardMarkup]]] = get_empty_reply_markup,
) -> StageType:
    class SimpleGetStage(Stage):
        state = State(state=stage_name)
        name: str = stage_name

        @staticmethod
        async def prepare(state: FSMContext) -> None:
            await Stage.bot.send_message(
                await get_id(state),
                text=question_text,
                reply_markup=await question_reply_markup_getter(state),
            )

        @staticmethod
        async def process(
            message: Message,
            state: FSMContext,
        ) -> None:
            await User.update_field(
                id=await get_id(state),
                field_name=SimpleGetStage.field_name,
                value=data_update_value_getter(message),
            )
            await SimpleGetStage.next_stage.prepare(state)
            # await state.update_data(**{stage_name: data_update_value_getter(message)})
            # await next_stage(SimpleGetStage, state)

        @staticmethod
        async def process_invalid_age(message: Message):
            await message.reply(invalid_value_text)

        @staticmethod
        def register(router: Router) -> None:
            router.message.register(
                SimpleGetStage.process,
                message_filter,
                SimpleGetStage.state,
            )

            router.message.register(
                SimpleGetStage.process_invalid_age,
                SimpleGetStage.state,
            )

    return SimpleGetStage


import logging
from utils import get_id, send_reply_keyboard
from stage import Stage, get_stage_logger
from typing import Type
from user_engine import update_field

from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, BaseFilter


def produce_field_stage(
    stage_name_arg: str,
    prepare_text_arg: str,
    value_getter_arg,
    inline_kb_getter_arg,
    reply_kb_getter_arg,
    invalid_value_text_arg: str,
    filter_arg: BaseFilter,
    allow_go_back_arg: bool,
) -> Type[Stage]:
    """A trick to produce many stage classes"""
    class FieldStage(Stage):
        """Basis for a stage that fills some field of user data"""
        stage_name: str = stage_name_arg
        state = State(state=stage_name_arg)
        _logger = get_stage_logger(stage_name=stage_name_arg)
        _prepare_state = State(state="prepare_" + stage_name_arg)
        _process_state = State(state="process_" + stage_name_arg)

        _GO_BACK_TEXT: str = "назад"

        @staticmethod
        async def _get_reply_kb(state: FSMContext) -> ReplyKeyboardMarkup:
            result = await reply_kb_getter_arg(state)
            if allow_go_back_arg:
                append_button(result, text=_GO_BACK_TEXT)
            return result

        @staticmethod
        async def prepare(state: FSMContext):
            """Prepare stage"""
            await state.set_state(FieldStage._prepare_state)

            result = await Stage.bot.send_messaage(
                await get_id(state),
                prepare_text_arg,
                reply_markup=await inline_kb_getter_arg(state),
            )

            await send_reply_keyboard(
                id=await get_id(state),
                keyboard=await FieldStage._get_reply_kb(state),
            )

            await state.set_state(FieldStage.state)

            FieldStage._logger.debug(
                "prepared stage for id=%s", await get_id(state))

            return result

        @staticmethod
        async def _process_set_field(
            message: Message, state: FSMContext
        ):
            """Process update of user's field and got to next stage"""
            await state.set_state(FieldStage._process_state)

            await update_field(
                id=await get_id(state),
                value=await value_getter_arg(message)
            )

            FieldStage._logger.debug(
                "set field for id=%s", await get_id(state))

            return await FieldStage.next_stage.prepare(state)

        @staticmethod
        async def _process_go_back(
            message: Message, state: FSMContext
        ):
            """Return to previous stage"""
            # TODO: remove keyboard reply
            return await FieldStage.prev_stage.prepare(state)

        @staticmethod
        async def _process_invalid_value(
            message: Message, state: FSMContext
        ):
            """User passed invalid value"""
            return await message.answer(invalid_value_text_arg)

        @staticmethod
        def register(router: Router) -> None:
            """Register handlers"""
            if allow_go_back_arg:
                router.message.register(
                    FieldStage._process.process_go_back,
                    Text(FieldStage._GO_BACK_TEXT),
                    FieldStage.state,
                )

            router.message.register(
                FieldStage._process_set_field,
                filter_arg,
                FieldStage.state,
            )

            router.message.register(
                FieldStage._process_invalid_value,
                FieldStage.state,
            )
