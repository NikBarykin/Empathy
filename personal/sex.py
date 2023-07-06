from constants import SEXES
from user_state import UserState

from aiogram import types
from aiogram.fsm.context import FSMContext


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
    await state.update_data(sex=message.text)

    await message.answer("В каком городе ты живешь?")
    await state.set_state(UserState.city)


async def process_invalid_sex(message: types.Message):
    await message.reply("Некорректное значение")
