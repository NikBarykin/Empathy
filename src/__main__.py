import asyncio
import logging

from aiogram import Bot, Dispatcher

# Stages
from stage import Stage

# TODO: move these imports to user_stages.config.imports

# This import initializes user-stages
from user_stages.config import configure

# import stages.moderation.config

from database.config import DATABASE_URL
from database.base import Base
from database.engine import (
    construct_async_engine,
    get_async_sessionmaker,
    proceed_schemas,
)

from bot.setup import setup_bot
from dispatcher.setup import setup_dispatcher


def configure_logging() -> None:
    """Make a basic configuration for logging"""
    logging.basicConfig(
        # TODO: change to WARNING when run on prod
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


async def main() -> None:
    """Main function of bot application"""
    configure_logging()

    bot: Bot = await setup_bot()

    dispatcher: Dispatcher = setup_dispatcher()

    engine = construct_async_engine(DATABASE_URL)

    await proceed_schemas(engine, Base.metadata)

    # setup global variables
    Stage.async_session = get_async_sessionmaker(engine)

    # run bot
    await dispatcher.start_polling(bot)

    # clean-up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
