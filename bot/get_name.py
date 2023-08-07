from aiogram.fsm.context import FSMContext


__key = "name"


async def set_name(state: FSMContext, name: str) -> None:
    await state.update_data(**{__key: name})


async def get_name(state: FSMContext) -> str:
    return (await state.get_data())[__key]


async def get_name_or_none(state: FSMContext) -> str:
    return (await state.get_data()).get(__key)
