from aiogram.filters.callback_data import CallbackData
from aiogram import Router


async def dummy_process_callback(*args, **kwargs):
    pass


class DummyCallbackFactory(CallbackData, prefix="dummy_does_nothing"):
    pass


def register_dummy_process_callback(router: Router):
    router.callback_query.register(
        dummy_process_callback,
        DummyCallbackFactory.filter(),
    )
