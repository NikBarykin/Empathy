# redis
from aioredis import Redis

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from user_stages.config.registration import register_user_stages
from utils.dummy import register_dummy_process_callback


def setup_dispatcher() -> Dispatcher:
    """Create dispatcher and register stages"""
    redis = Redis()
    dispatcher = Dispatcher(storage=RedisStorage(redis=redis))
    register_user_stages(dispatcher)
    register_dummy_process_callback(dispatcher)

    return dispatcher
