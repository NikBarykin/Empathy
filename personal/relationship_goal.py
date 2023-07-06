from constants import RELATIONSHIP_GOALS
from user_state import UserState

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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

    # photo
    await message.answer(
            "Добавьте свою фотографию",
            reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.photo)


async def process_invalid_relationship_goal(
        message: types.Message,
        ):
    message.reply(
            "Некорректное значение",
            reply_markup=get_kb(),
            )
