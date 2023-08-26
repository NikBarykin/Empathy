"""Go to previous stage"""
from stages.stage import Stage, go_stage
from typing import Type

from aiogram import F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.fsm.context import FSMContext

from .keyboard import send_reply_kb


async def go_prev_stage(
    departure: Type[Stage],
    state: FSMContext,
):
    return await go_stage(
        departure=departure,
        destination=departure.prev_stage,
        state=state,
    )


PREV_STAGE_TEXT: str = "Назад"
PREV_STAGE_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=PREV_STAGE_TEXT)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def send_prev_stage_keyboard(chat_id: int):
    return await send_reply_kb(chat_id=chat_id, kb=PREV_STAGE_KB)


def make_prev_stage_processor(departure_stage: Type[Stage]):
    async def process_go_prev_stage(_: Message, state: FSMContext):
        return await go_prev_stage(
            departure=departure_stage,
            state=state,
        )
    return process_go_prev_stage


PREV_STAGE_FILTER = F.text==PREV_STAGE_TEXT
