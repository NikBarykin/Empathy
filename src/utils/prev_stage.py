"""Go to previous stage"""
from stage import Stage
from typing import Type

from aiogram import F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.fsm.context import FSMContext

from utils.keyboard import send_reply_kb, RowKeyboard


PREV_STAGE_TEXT: str = "Назад"
PREV_STAGE_KB = RowKeyboard(PREV_STAGE_TEXT)


async def send_prev_stage_keyboard(chat_id: int):
    return await send_reply_kb(chat_id=chat_id, kb=PREV_STAGE_KB)


def make_prev_stage_processor(departure_stage: Type[Stage]):
    async def process_go_prev_stage(_: Message, state: FSMContext):
        return departure_stage.prev_stage.prepare(state)
    return process_go_prev_stage


PREV_STAGE_FILTER = F.text==PREV_STAGE_TEXT
