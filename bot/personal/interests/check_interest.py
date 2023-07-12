from user_state import UserState

from personal import photo
from personal.interests.prepare import (
        get_inline_kb,
        get_interests,
        get_interests_text,
        )

from constants import (
        INTERESTS,
        NO_INTERESTS,
        CHECK_MARK_EMOJI,
        )

from typing import Set

from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def process_callback_check_interest(
        callback: types.CallbackQuery,
        state: FSMContext,
        ):
    interests = await get_interests(state)
    target_interest = callback.data.split('_', maxsplit=1)[1]

    if target_interest in interests:
        interests.remove(target_interest)
    else:
        if len(interests) == NO_INTERESTS:
            # Too much interests

            await callback.answer(text="Превышено допустимое количество интересов")
            return 

        interests.add(target_interest)

    await state.update_data(interests=interests)

    await callback.message.edit_text(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )
    await callback.answer()
