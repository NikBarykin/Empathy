import asyncio
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup

from aiogram.filters.command import Command

from random import randint

from bot_config import TOKEN

from dataclasses import dataclass

import sys

from agent import Agent

from setup import load_from_file

from search import search

import form
import match

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

agents = dict()

class Form(StatesGroup):
    age = State()
    gender = State()
    picture = State()
    registered = State()


@dp.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.set_state(Form.age)
    await msg.reply("How old are you?")


@dp.message(Form.age)
async def process_age(msg: types.Message, state: FSMContext):
    await state.set_state(Form.gender)

    await state.update_data(age=int(msg.text))

    kb = [
            [types.KeyboardButton(text="Male")],
            [types.KeyboardButton(text="Female")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await msg.reply("What is your gender?", reply_markup=keyboard)


AVAILABLE_GENDERS = ['Male', 'Female']

@dp.message(
        Form.gender,
        F.text.in_(AVAILABLE_GENDERS)
)
async def process_gender(msg: types.Message, state: FSMContext):
    await state.update_data(gender=msg.text)
    await state.set_state(Form.picture)

    await msg.reply("What do you look like?")

@dp.message(
        F.photo,
        Form.picture
)
async def process_photo(msg: types.Message, state: FSMContext):

    await state.update_data(picture=msg.photo[0].file_id)

    user_data = await state.get_data()

    user_id = msg.from_user.id
    user_name = msg.from_user.username

    new_agent = Agent(
            user_id,
            user_name,
            user_data['age'],
            user_data['gender'],
            user_data['picture'])

    agents[new_agent.user_id] = new_agent

    markup = types.ReplyKeyboardRemove()

    await bot.send_message
            msg.chat.id,
            text=f"{new_agent.user_name}, you look beautiful!",
            reply_markup=markup)

    await bot.send_photo(
            msg.chat.id,
            new_agent.picture,
            reply_markup=markup)

    await state.set_state(Form.registered)


@dp.message(Command('search'), Form.registered)
async def process_search(msg: types.Message):
    user_id = msg.from_user.id
    agent = agents[user_id]

    candidates = search(agent, agents.values())
    candidates_str = '\n'.join(map(str, candidates))

    await msg.reply(f"Found these agents:{candidates_str}")


async def main():
    global agents
    agents = load_from_file("setup.txt")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
