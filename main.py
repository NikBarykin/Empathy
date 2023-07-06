from database_declarative_base import Base

import command_start
import personal
import preference
import matching

import asyncio
import logging

# sqlalchemy
# asyncio
from sqlalchemy.ext.asyncio import (
        create_async_engine,
        async_sessionmaker,
        )

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN


async def main():
    # logging to sdout
    logging.basicConfig(
            level = logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )

    storage = MemoryStorage()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_router(command_start.router)
    dp.include_router(personal.router)
    dp.include_router(preference.router)
    dp.include_router(matching.router)

    # TODO: command-line-argument
    engine = create_async_engine(
            "sqlite+aiosqlite:///database.db",
            echo=True,
            )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, async_session=async_session)

    # clean-up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
