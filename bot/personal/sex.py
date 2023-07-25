from simple_get_stage import produce_simple_get_stage
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message
from constants import SEXES
from stage import Stage
from text_lower_data_update_value_getter import text_lower_data_update_value_getter
from one_alternative_from_filter import OneAlternativeFromFilter


async def get_kb(_: FSMContext) -> types.ReplyKeyboardMarkup:
    kb = [
            [types.KeyboardButton(text=sex) for sex in SEXES]
    ]
    return types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            )


SexStage = produce_simple_get_stage(
    stage_name="пол",
    question_text="Твой пол?",
    question_reply_markup_getter=get_kb,
    invalid_value_text=f"Принимаются только значения {SEXES}",
    data_update_value_getter=text_lower_data_update_value_getter,
    message_filter=OneAlternativeFromFilter(SEXES),
)
