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
            await state.update_data(**{stage_name: data_update_value_getter(message)})
            await next_stage(SimpleGetStage, state)

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
