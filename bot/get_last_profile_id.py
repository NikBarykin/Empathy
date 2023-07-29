from get_id import get_id
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

from typing import Optional


__key = "last_profile_id"


async def set_last_profile_id(state: FSMContext, profile_id: Optional[int]) -> None:
    await state.update_data(**{__key: profile_id})


async def __get_last_profile_id(state: FSMContext) -> Optional[int]:
    return (await state.get_data()).get(__key)


async def delete_last_profile(bot: Bot, state: FSMContext) -> None:
    last_profile_id = await __get_last_profile_id(state)
    if last_profile_id is None:
        return

    with suppress(TelegramBadRequest):
        await bot.delete_message(
            chat_id=await get_id(state),
            message_id=last_profile_id,
        )

        await set_last_profile_id(state, None)
