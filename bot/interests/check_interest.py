from typing import Set

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from constants import CHECK_MARK_EMOJI, INTERESTS, NO_INTERESTS
# from personal import photo
from user_state import UserState

from .prepare import get_inline_kb, get_interests, get_interests_text, get_interests_key


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

            await callback.answer(
                text="Превышено допустимое количество интересов")
            return

        interests.add(target_interest)

    await state.update_data(
        **{(await get_interests_key(state)): (await get_interests(state))}
    )

    await callback.message.edit_text(
            text=await get_interests_text(state),
            reply_markup=await get_inline_kb(state),
            )
    await callback.answer()
