from user_state import UserState

from personal import photo

from personal.interests.prepare import (
        get_interests,
        )

from constants import (
        INTERESTS,
        NO_INTERESTS,
        CHECK_MARK_EMOJI,
        )

from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_inline_kb(
        state: FSMContext,
        ) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for interest in await get_interests(state):
        builder.button(
                text=interest + CHECK_MARK_EMOJI,
                # no callback
                callback_data="pass",
                )

    builder.adjust(1)
    return builder.as_markup()

async def process_submit(
        message: Message,
        state: FSMContext,
        ) -> None:
    await message.edit_text(
            text="Выбранные интересы:",
            reply_markup=await get_inline_kb(state),
            )


async def process_callback_submit(
        callback: types.CallbackQuery,
        state: FSMContext,
        ):
    interests = await get_interests(state)

    if len(interests) < NO_INTERESTS:
        await callback.answer(
                text=f"Недостаточно интересов (должно быть {NO_INTERESTS})")
        return

    await process_submit(
            callback.message,
            state,
            )

    await callback.answer()

    # photo
    await photo.prepare(
            callback.message,
            state,
            )
