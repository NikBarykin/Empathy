from aiogram.fsm.context import FSMContext


async def get_id(state: FSMContext) -> int:
    return (await state.get_data())['id']
