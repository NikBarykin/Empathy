import time
from typing import Set

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from constants import (CHECK_MARK_EMOJI, INTEREST_PAGES, INTERESTS,
                       NO_INTEREST_PAGES, NO_INTERESTS)
# from personal import photo
from user_state import UserState


async def get_interests_key(state: FSMContext) -> str:
    return ("interests" if (await state.get_state()) == UserState.interests
            else "preferred_partner_interests")

async def get_interests(state: FSMContext) -> Set[str]:
    return (await state.get_data())[await get_interests_key(state)]


async def partner_interests(state: FSMContext) -> bool:
    return (await state.get_state()) == UserState.preferred_partner_interests


async def get_interests_text(state: FSMContext) -> str:
    return (f"Отметь свои интересы и нажми \"подтвердить\" ({NO_INTERESTS} шт.)"
            if not await partner_interests(state)
            else f"Интересы партнера ({NO_INTERESTS} шт.)")


async def get_inline_kb(state: FSMContext) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    checked_interests = await get_interests(state)
    interest_page_i: int = (await state.get_data())['interest_page_i']

    for interest in INTEREST_PAGES[interest_page_i]:
        postscript = (CHECK_MARK_EMOJI if interest in checked_interests
                      else "")

        builder.button(
                text=interest + postscript,
                callback_data=f"interest_{interest}",
                )

    builder.adjust(2)

    if interest_page_i == 0:
        left_arrow_button = InlineKeyboardButton(
            text="✖️",
            callback_data="pass",
        )
    else:
        left_arrow_button = InlineKeyboardButton(
            text="⬅️",
            callback_data=f"gopage_{interest_page_i - 1}",
        )

    page_index_button = InlineKeyboardButton(
        text=f"{interest_page_i + 1}/{NO_INTEREST_PAGES}",
        callback_data="pass",
    )

    if interest_page_i + 1 == NO_INTEREST_PAGES:
        right_arrow_button = InlineKeyboardButton(
            text="✖️",
            callback_data="pass",
        )
    else:
        right_arrow_button = InlineKeyboardButton(
            text="➡",
            callback_data=f"gopage_{interest_page_i + 1}",
        )

    builder.row(
        left_arrow_button,
        page_index_button,
        right_arrow_button,
    )

    # "submit" button
    builder.row(
            InlineKeyboardButton(
                text="📍подтвердить📍",
                callback_data="submit_interests",
            )
        )

    if await partner_interests(state):
        builder.row(
            InlineKeyboardButton(
                text="подтвердить такие же интересы, как у меня",
                callback_data="submit_interests_same",
            )
        )

    return builder.as_markup()


async def process_callback_go_page(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    page_i: int = int(callback.data.split('_', maxsplit=1)[1])
    await state.update_data(interest_page_i=page_i)

    await callback.message.edit_text(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )
    await callback.answer()


async def prepare_interests(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(interests=set(), interest_page_i=0)
    await state.set_state(UserState.interests)
    await message.answer(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )


async def prepare_preferred_partner_interests(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(preferred_partner_interests=set(), interest_page_i=0)
    await state.set_state(UserState.preferred_partner_interests)

    await message.answer(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )
