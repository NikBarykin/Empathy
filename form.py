import asyncio
import logging

# aiogram
from aiogram import Router, F
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from user_state import AgentState
from agent import Agent, AVAILABLE_GENDERS, AVAILABLE_CITIES, RELATIONSHIP_GOALS
from match import get_match_command_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.update_data(user_id=msg.from_user.id)
    await state.update_data(username=msg.from_user.username)
    await msg.answer("Как Вас зовут?")
    await state.set_state(AgentState.name)


@router.message(
        F.text,
        AgentState.name)
async def process_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Сколько Вам лет?")
    await state.set_state(AgentState.age)


def get_gender_kb() -> types.ReplyKeyboardMarkup:
    kb = [
            [types.KeyboardButton(text=gender) for gender in AVAILABLE_GENDERS]
    ]
    return types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            )


# TODO: improve filter (for example age thresholds)
@router.message(
        F.text.isnumeric(),
        AgentState.age)
async def process_age(msg: types.Message, state: FSMContext):
    await state.update_data(age=int(msg.text))
    await msg.answer(
            "Ваш пол?",
            reply_markup=get_gender_kb())
    await state.set_state(AgentState.gender)


@router.message(AgentState.age)
async def process_incorrect_age(msg: types.Message):
    await msg.reply("Некорректное значение")


@router.message(
        AgentState.gender,
        F.text.lower().in_(AVAILABLE_GENDERS)
)
async def process_gender(msg: types.Message, state: FSMContext):
    await state.update_data(gender=msg.text)
    await msg.answer("В каком городе Вы проживаете?")
    await state.set_state(AgentState.city)


@router.message(
        AgentState.gender
)
async def process_invalid_gender(msg: types.Message):
    await msg.reply("Некорректное значение")


# TODO: allow mistakes and add more cities
@router.message(
        F.text.lower().in_(AVAILABLE_CITIES),
        AgentState.city,
)
async def process_city(msg: types.Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await msg.answer(
            "Ваша цель",
            reply_markup=get_relationship_goal_kb()
            )
    await state.set_state(AgentState.relationship_goal)

def get_relationship_goal_kb() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for goal in RELATIONSHIP_GOALS:
        builder.button(text=goal)
    builder.adjust(2)
    return builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
            )

@router.message(
        F.text.lower().in_(RELATIONSHIP_GOALS),
        AgentState.relationship_goal
        )
async def process_relationship_goal(msg: types.Message, state: FSMContext):
    await msg.answer(
            "Добавьте свою фотографию",
            reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AgentState.picture)


@router.message(
        AgentState.city
)
async def process_invalid_city(msg: types.Message):
    await msg.reply("Я не знаю такого города")


# TODO: multiple pictures
@router.message(
        F.photo,
        AgentState.picture
)
async def process_photo(msg: types.Message, state: FSMContext):
    await state.update_data(picture=msg.photo[0].file_id)

    await msg.reply("Отлично выглядите!")
    await msg.answer("Напишите немного о себе в свободной форме (не более 240 символов)")

    await state.set_state(AgentState.about_yourself)

# TODO: ограничениие на размер текста
@router.message(
        F.text.len() < 240,
        AgentState.about_yourself,
        )
async def process_about_yourself(msg: types.Message, state: FSMContext):
    await state.update_data(about_yourself=msg.text)
    await msg.answer("Укажите минимальный возраст партнера")
    await state.set_state(AgentState.min_preferred_age)

@router.message(
        F.text,
        AgentState.about_yourself,
        )
async def process_about_yourself(msg: types.Message):
    await msg.reply("Слишном длинное описание")
