from aiogram import types
from aiogram.fsm.context import FSMContext
from constants import SEXES
from user_state import UserState

from personal import city


def get_kb() -> types.ReplyKeyboardMarkup:
    kb = [
            [types.KeyboardButton(text=sex) for sex in SEXES]
    ]
    return types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            )


async def process_sex(
        message: types.Message,
        state: FSMContext
        ):
    await state.update_data(sex=message.text.lower())
    await city.prepare(message, state)


async def process_invalid_sex(message: types.Message):
    await message.reply("Некорректное значение")
