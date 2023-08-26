from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData


async def dummy_process_callback(callback: CallbackQuery, *args, **kwargs):
    """Dummy just answers callback"""
    await callback.answer()


class DummyCallbackFactory(CallbackData, prefix="dummy_does_nothing"):
    """Empty callback factory"""
    pass


def register_dummy_process_callback(router: Router):
    """Register dummy"""
    router.callback_query.register(
        dummy_process_callback,
        DummyCallbackFactory.filter(),
    )
