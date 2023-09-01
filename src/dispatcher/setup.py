# redis
from aioredis import Redis

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from user_stages.config import USER_STAGES
from moderation_stages.config import MODERATION_STAGES

from utils.dummy import register_dummy_process_callback


def setup_dispatcher() -> Dispatcher:
    """Create dispatcher and register stages"""
    redis = Redis()
    dispatcher = Dispatcher(storage=RedisStorage(redis=redis))

    for stage in MODERATION_STAGES + USER_STAGES:
        stage.register(dispatcher)

    register_dummy_process_callback(dispatcher)

    return dispatcher
