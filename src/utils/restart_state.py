from aiogram.fsm.context import FSMContext

from utils.id import ID_KEY


async def restart_state(state: FSMContext, user_id: int) -> None:
    """Restart state. Can be used when user entered '/start' or '/moderate_...'"""
    await state.clear()
    await state.set_data({ID_KEY: user_id})
