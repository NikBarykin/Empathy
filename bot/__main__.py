from db.base import Base

import command_start
import personal
import preference
import matching

import asyncio
import logging

import sys

# sqlalchemy
# asyncio
from sqlalchemy.ext.asyncio import (
        create_async_engine,
        async_sessionmaker,
        )

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.engine import URL

from config import (
        TOKEN,
        DATABASE_PATH,
        )

async def bot_start(logger: logging.Logger) -> None:
    # logging to sdout
    logging.basicConfig(
            # TODO: change to WARNING
            level = logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )

    storage = MemoryStorage()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_router(command_start.router)
    dp.include_router(personal.router)
    dp.include_router(preference.router)
    dp.include_router(matching.router)

    postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username="nikita",
        host="localhost",
        port=5432,
        database="database.db",
    )

    engine = create_async_engine(
        postgres_url,
        echo=True,
        # encoding='utf-8',
        pool_pre_ping=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        async_session=async_session,
        logger=logger,
    )

    # clean-up
    await engine.dispose()


def main():
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(bot_start(logger))
        logger.info("Bot started")
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()
