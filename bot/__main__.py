import asyncio
import logging
import sys
from stages_initialization import init_stages

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.fsm.state import State, StatesGroup, any_state
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.loggers import event as event_logger

from sqlalchemy.engine import URL
# sqlalchemy
# asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Stages
from stage import Stage
from command_start import StartStage

# Personal
from personal.name import NameStage
from personal.age import AgeStage
from personal.sex import SexStage
from personal.city import CityStage
from personal.relationship_goal import RelationshipGoalStage
from interests.preferred_interests import PreferredInterestsStage
from personal.photo import PhotoStage
from personal.self_description import SelfDescriptionStage

# Preferences
from preference.min_preferred_age import MinPreferredAgeStage
from preference.max_preferred_age import MaxPreferredAgeStage
from interests.personal_interests import PersonalInterestsStage

from register_stage import RegisterStage
from matching.stage import MatchStage

# overwrite
from overwrite.start import OverwriteStartStage
from overwrite.personal import OverwritePersonalStage
from overwrite.preference import OverwritePreferenceStage

from config import DATABASE_URL, TOKEN
from db.base import Base
from db.engine import (construct_async_engine, get_async_sessionmaker,
                       proceed_schemas)

# redis
from aioredis import Redis

from dummy_callback_factory import register_dummy_process_callback
from notify_everyone_on_start import notify_everyone_on_start


def configure_logging() -> None:
    # logging to sdout
    logging.basicConfig(
        # TODO: change to WARNING when run on prod
        level = logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # logging for aiogram events
    event_handler = logging.FileHandler("sueta.log", mode="a")
    event_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    event_handler.setFormatter(event_formatter)
    event_logger.addHandler(event_handler)


async def bot_start(logger: logging.Logger) -> None:
    configure_logging()

    # TODO: redis
    redis = Redis()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    Stage.bot = bot

    init_stages(
        router=dp,
        start_stage=StartStage,
        personal_stages=[
            NameStage,
            AgeStage,
            SexStage,
            CityStage,
            RelationshipGoalStage,
            PersonalInterestsStage,
            PhotoStage,
            SelfDescriptionStage,
        ],
        preference_stages=[
            MinPreferredAgeStage,
            MaxPreferredAgeStage,
            # PreferredInterestsStage,
        ],
        register_stage=RegisterStage,
        match_stage=MatchStage,
        overwrite_stages=[
            OverwriteStartStage,
            OverwritePersonalStage,
            OverwritePreferenceStage,
        ],
        )

    register_dummy_process_callback(dp)

    engine = construct_async_engine(DATABASE_URL)

    await proceed_schemas(engine, Base.metadata)

    Stage.async_session = get_async_sessionmaker(engine)

    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(
        bot,
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
