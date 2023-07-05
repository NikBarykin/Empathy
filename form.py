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

from user_state import UserState
from agent import Agent, AVAILABLE_GENDERS, AVAILABLE_CITIES, RELATIONSHIP_GOALS
from match import get_match_command_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(username=message.from_user.username)
    await message.answer("Как Вас зовут?")
    await state.set_state(UserState.name)


@router.message(
        F.text,
        UserState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько Вам лет?")
    await state.set_state(UserState.age)


def get_sex_kb() -> types.ReplyKeyboardMarkup:
    kb = [
            [types.KeyboardButton(text=sex) for sex in AVAILABLE_GENDERS]
    ]
    return types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            )


# TODO: improve filter (for example age thresholds)
@router.message(
        F.text.isnumeric(),
        UserState.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer(
            "твой пол?",
            reply_markup=get_sex_kb())
    await state.set_state(UserState.sex)


@router.message(UserState.age)
async def process_incorrect_age(message: types.Message):
    await message.reply("Некорректное значение")


@router.message(
        UserState.sex,
        F.text.lower().in_(AVAILABLE_GENDERS)
)
async def process_sex(message: types.Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await message.answer("В каком городе ты проживаете?")
    await state.set_state(UserState.city)


@router.message(
        UserState.sex
)
async def process_invalid_sex(message: types.Message):
    await message.reply("Некорректное значение")


# TODO: allow mistakes and add more cities
@router.message(
        F.text.lower().in_(AVAILABLE_CITIES),
        UserState.city,
)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer(
            "Твоя цель",
            reply_markup=get_relationship_goal_kb()
            )
    await state.set_state(UserState.relationship_goal)

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
        UserState.relationship_goal
        )
async def process_relationship_goal(message: types.Message, state: FSMContext):
    await state.update_data(relationship_goal=message.text)
    await message.answer(
            "Добавьте свою фотографию",
            reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.picture)


@router.message(
        UserState.city
)
async def process_invalid_city(message: types.Message):
    await message.reply("Я не знаю такого города")


# TODO: multiple pictures
@router.message(
        F.photo,
        UserState.picture
)
async def process_photo(message: types.Message, state: FSMContext):
    await state.update_data(picture=message.photo[0].file_id)

    await message.reply("Отлично выглядите!")
    await message.answer("Напишите немного о себе в свободной форме (не более 240 символов)")

    await state.set_state(UserState.about_yourself)

@router.message(
        F.text.len() < 240,
        UserState.about_yourself,
        )
async def process_about_yourself(message: types.Message, state: FSMContext):
    await state.update_data(about_yourself=message.text)
    await message.answer("Укажите минимальный возраст партнера")
    await state.set_state(UserState.min_preferred_age)


@router.message(
        F.text,
        UserState.about_yourself,
        )
async def process_about_yourself(message: types.Message):
    await message.reply("Слишном длинное описание")
