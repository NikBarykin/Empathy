from aiogram.fsm.context import FSMContext


name_key = "name_key"


async def set_name(state: FSMContext, name: str) -> None:
    await state.update_data(**{name_key: name})


async def get_name(state: FSMContext) -> None:
    return (await state.get_data())[name_key]
