import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.engine import URL
# sqlalchemy
# asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import command_start
import matching
import personal
import preference
from config import DATABASE_URL, TOKEN
from db.base import Base
from db.engine import (construct_async_engine, get_async_sessionmaker,
                       proceed_schemas)


def include_all_routers(dp: Dispatcher) -> None:
    dp.include_router(command_start.router)
    dp.include_router(personal.router)
    dp.include_router(preference.router)
    dp.include_router(matching.router)


def configure_logging() -> None:
    # logging to sdout
    logging.basicConfig(
        # TODO: change to WARNING when run on prod
        level = logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

async def bot_start(logger: logging.Logger) -> None:
    configure_logging()

    # TODO: redis
    storage = MemoryStorage()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    include_all_routers(dp)

    engine = construct_async_engine(DATABASE_URL)

    await proceed_schemas(engine, Base.metadata)

    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(
        bot,
        async_session=get_async_sessionmaker(engine),
        logger=logger,
    )

    # clean-up
    await engine.dispose()


def main():
    logger = logging.getLogger(__name__)
    try:
        logger.info("Bot started")
        asyncio.run(bot_start(logger))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()
