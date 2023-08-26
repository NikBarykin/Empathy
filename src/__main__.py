import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import BotCommand
from aiogram.fsm.state import State, StatesGroup, any_state
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.engine import URL
# sqlalchemy
# asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# redis
from aioredis import Redis

# Stages
from stages.stage import Stage

# TODO: move these imports to stages.regular_workflow.config.imports
from stages.regular_workflow.config.declarations import all_stages
from stages.regular_workflow.config import order
from stages.regular_workflow.config.registration import register_stages as register_regular_stages

from stages.regular_workflow.profile import ProfileStage

# import stages.moderation.config
from utils.dummy import register_dummy_process_callback

from config import DATABASE_URL, TOKEN

from db.base import Base
from db.engine import (
    construct_async_engine,
    get_async_sessionmaker,
    proceed_schemas,
)


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

    redis = Redis()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    # register stages for regular workflow
    register_regular_stages(dp)

    # register dummy-callback
    register_dummy_process_callback(dp)

    engine = construct_async_engine(DATABASE_URL)

    await proceed_schemas(engine, Base.metadata)

    # setup global variables
    Stage.bot = bot
    Stage.async_session = get_async_sessionmaker(engine)

    # setup commands
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command=ProfileStage.name, description=ProfileStage.description)
        ]
    )

    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)

    # run bot
    await dp.start_polling(bot)

    # clean-up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
