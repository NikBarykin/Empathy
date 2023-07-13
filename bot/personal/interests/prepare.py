from typing import Set

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from constants import CHECK_MARK_EMOJI, INTERESTS, NO_INTERESTS
from personal import photo
from user_state import UserState


async def get_interests(state: FSMContext) -> Set[str]:
    return (await state.get_data())['interests']


async def get_interests_text(state: FSMContext) -> str:
    return f"Твои интересы ({NO_INTERESTS} шт.): "


async def get_inline_kb(state: FSMContext) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    checked_interests = await get_interests(state)

    for interest in INTERESTS:
        postscript = (CHECK_MARK_EMOJI if interest in checked_interests
                      else "")

        builder.button(
                text=interest + postscript,
                callback_data=f"interest_{interest}",
                )

    builder.adjust(2)

    # "submit" button
    builder.row(
            InlineKeyboardButton(
                text="📍подтвердить📍",
                callback_data="submit_interests",
            )
        )

    return builder.as_markup()


async def prepare_interests(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(interests=set())
    await message.answer(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )
    await state.set_state(UserState.interests)
