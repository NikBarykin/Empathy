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

from setup import load_from_file

from search import search

import process_help
import form
import match


async def main():
    storage = MemoryStorage()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_routers(process_help.router, form.router, match.router)

    agents = load_from_file("setup.txt")

    await dp.start_polling(bot, agents=agents)


if __name__ == "__main__":
    asyncio.run(main())
