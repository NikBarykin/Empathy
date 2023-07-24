from stage_order import next_stage

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import State

from constants import RELATIONSHIP_GOALS


async def get_kb(state: FSMContext) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for goal in RELATIONSHIP_GOALS:
        builder.button(text=goal)

    builder.adjust(2)

    return builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
            )

from simple_get_stage import produce_simple_get_stage
from one_alternative_from_filter import OneAlternativeFromFilter


RelationshipGoalStage = produce_simple_get_stage(
    stage_name="цель отношений",
    question_text="Цель отношений?",
    question_reply_markup_getter=get_kb,
    invalid_value_text="Неизвестное значение",
    data_update_value_getter=lambda message: message.text,
    message_filter=OneAlternativeFromFilter(RELATIONSHIP_GOALS),
)
