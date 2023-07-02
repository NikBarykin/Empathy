import asyncio
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from bot_config import TOKEN

import sys

from setup import load_from_file

import process_help
import form
import preferences
import match


async def main():
    storage = MemoryStorage()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_routers(
            process_help.router,
            form.router,
            preferences.router,
            match.router)

    # TODO: set instead of map
    agents = load_from_file("setup.txt")

    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, agents=agents)


if __name__ == "__main__":
    asyncio.run(main())
