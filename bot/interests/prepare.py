import time
from typing import Set

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from constants import CHECK_MARK_EMOJI, INTERESTS, NO_INTERESTS
from personal import photo
from user_state import UserState


async def get_interests(state: FSMContext) -> Set[str]:
    key: str = ("interests" if (await state.get_state()) == UserState.interests
                else "preferred_partner_interests")
    return (await state.get_data())[key]


async def partner_interests(state: FSMContext) -> bool:
    return (await state.get_state()) == UserState.preferred_partner_interests


async def get_interests_text(state: FSMContext) -> str:
    return (f"Твои интересы ({NO_INTERESTS} шт.)"
            if not await partner_interests(state)
            else f"Интересы партнера({NO_INTERESTS} шт.)")


async def get_inline_kb(state: FSMContext) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    checked_interests = await get_interests(state)

    for interest in INTERESTS[:40]:
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

    if await partner_interests(state):
        builder.row(
            InlineKeyboardButton(
                text="подтвердить такие же интересы, как у меня",
                callback_data="submit_interests_same",
            )
        )

    return builder.as_markup()


async def prepare_interests(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(interests=set())
    await state.set_state(UserState.interests)
    # for interest in INTERESTS:
    #     time.sleep(0.2)
    #     print(interest)
    #     builder = InlineKeyboardBuilder()
    #     builder.button(text=interest, callback_data="pass")
    #     await message.answer(
    #         text="text",
    #         reply_markup=builder.as_markup(),
    #     )
    await message.answer(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )


async def prepare_preferred_partner_interests(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(preferred_partner_interests=set())
    await state.set_state(UserState.preferred_partner_interests)

    await message.answer(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )
