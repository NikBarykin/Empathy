from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from constants import RELATIONSHIP_GOALS
from interests.prepare import prepare_interests
from user_state import UserState


def get_kb() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for goal in RELATIONSHIP_GOALS:
        builder.button(text=goal)

    builder.adjust(2)

    return builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
            )


async def process_relationship_goal(
        message: types.Message,
        state: FSMContext,
        ):
    await state.update_data(relationship_goal=message.text)

    await prepare_interests(message, state)


async def process_invalid_relationship_goal(
        message: types.Message,
        ):
    message.reply(
            "Некорректное значение",
            reply_markup=get_kb(),
            )
