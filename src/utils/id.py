from aiogram.fsm.context import FSMContext


ID_KEY: str = "id"


async def get_id(state: FSMContext) -> int:
    """Get user id from his state"""
    return (await state.get_data())[ID_KEY]
