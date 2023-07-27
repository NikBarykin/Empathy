from stage import Stage

from get_id import get_id
from get_name import get_name_or_none

from stage_order import next_stage

from aiogram import Router, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from typing import Optional


async def get_kb(state: FSMContext) -> Optional[ReplyKeyboardMarkup]:
    name: Optional[str] = await get_name_or_none(state)
    if name is None:
        return None
    else:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=name)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )


class NameStage(Stage):
    state = State()
    name: str = "имя"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await Stage.bot.send_message(
            await get_id(state),
            text="Как тебя зовут?",
            reply_markup=await get_kb(state),
        )

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            NameStage.process,
            # TODO: remove 32
            F.text.len() <= 32,
            NameStage.state,
        )

        router.message.register(
            NameStage.process_invalid_value,
            NameStage.state,
        )

    @staticmethod
    async def process(
        message: Message,
        state: FSMContext,
    ) -> None:
        await state.update_data(**{NameStage.name: message.text})
        await next_stage(NameStage, state)

    @staticmethod
    async def process_invalid_value(message: types.Message):
        await message.reply("Некорректное значение имени")
