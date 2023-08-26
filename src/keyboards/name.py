from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from filters.name import NameFilter


async def get_kb(state: FSMContext) -> ReplyKeyboardMarkup | None:
    """Reply keyboard for name stage"""
    name = (await state.get_data()).get('name')
    if name is not None and NameFilter.check(name):
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=name)
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
