import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from random import randint

from bot_config import TOKEN

from dataclasses import dataclass

import sys

from agent import Agent

from setup import load_from_file

from search import search

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

agents = dict()

class Form(StatesGroup):
    age = State()
    gender = State()
    registered = State()


@dp.message_handler(commands='start')
async def cmd_start(msg: types.Message):
    await Form.age.set()

    await msg.reply("How old are you?")


@dp.message_handler(state=Form.age)
async def process_age(msg: types.Message, state: FSMContext):
    await Form.next()

    await state.update_data(age=int(msg.text))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")

    await msg.reply("What is your gender?", reply_markup=markup)


AVAILABLE_GENDERS = ['Male', 'Female']

@dp.message_handler(
        lambda message: message.text in AVAILABLE_GENDERS,
        state=Form.gender)
async def process_gender(msg: types.Message, state: FSMContext):

    await state.update_data(gender=msg.text)

    user_data = await state.get_data()

    user_id = msg.from_user.id
    user_name = msg.from_user.username

    new_agent = Agent(user_id, user_name, user_data['age'], user_data['gender'])
    agents[new_agent.user_id] = new_agent

    markup = types.ReplyKeyboardRemove()

    await bot.send_message(
            msg.chat.id,
            f"Agent: {new_agent} successfully created!",
            reply_markup=markup)

    await Form.next()


@dp.message_handler(commands='search', state=Form.registered)
async def process_search(msg: types.Message):
    user_id = msg.from_user.id
    agent = agents[user_id]

    candidates = search(agent, agents.values())
    candidates_str = '\n'.join(map(str, candidates))

    await msg.reply(f"Found these agents:{candidates_str}")


def main():
    global agents
    agents = load_from_file("setup.txt")

    executor.start_polling(dp)


if __name__ == "__main__":
    main()
