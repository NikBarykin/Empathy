from aiogram.fsm.context import FSMContext


async def get_id(state: FSMContext) -> int:
    """Get user id from his state"""
    return (await state.get_data())['id']
