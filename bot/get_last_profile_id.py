from aiogram.fsm.context import FSMContext
from typing import Optional


__key = "last_profile_id"


async def set_last_profile_id(state: FSMContext, profile_id: int) -> None:
    await state.update_data(**{__key: profile_id})


async def get_last_profile_id(state: FSMContext) -> Optional[int]:
    return (await state.get_data()).get(__key)
