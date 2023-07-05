from user_state import UserState
from aiogram import Router, F

import asyncio
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.filters.command import Command

from search import search
from match_engine import find_match
import emoji
from match import get_match_command_keyboard

from aiogram.filters.callback_data import CallbackData

from agent import create_agent



router = Router()


# TODO: invalid value
@router.message(
        F.text.isnumeric(),
        UserState.min_preferred_age
        )
async def process_min_preferred_age(
        message: types.Message,
        state: FSMContext):
    await state.update_data(min_preferred_age=int(message.text))
    await message.answer("Укажите максимальный возраст партнера")
    await state.set_state(UserState.max_preferred_age)


@router.message(
        F.text.isnumeric(),
        UserState.max_preferred_age
        )
async def process_min_preferred_age(
        message: types.Message,
        state: FSMContext,
        agents):
    await state.update_data(max_preferred_age=int(message.text))

    new_agent = create_agent(await state.get_data())
    agents.add(new_agent)

    await message.answer(
            "Ты успешно зарегистрированы! Теперь тебе доступен подбор партнера.",
            reply_markup = get_match_command_keyboard())
    await state.set_state(UserState.registered)
