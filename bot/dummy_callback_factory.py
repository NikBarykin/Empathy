from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram import Router


async def dummy_process_callback(callback: CallbackQuery, *args, **kwargs):
    await callback.answer()


class DummyCallbackFactory(CallbackData, prefix="dummy_does_nothing"):
    pass


def register_dummy_process_callback(router: Router):
    router.callback_query.register(
        dummy_process_callback,
        DummyCallbackFactory.filter(),
    )
