import logging
from .base import BaseStage

from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PersonalInterestsStage(BaseStage):
    state = State()
    name: str = "твои интересы"
    question_text: str = "Отметь свои интересы"
    submit_text: str = "Твои отмеченные интересы"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await BaseStage.prepare_base(PersonalInterestsStage, state)

    @staticmethod
    async def process_callback_check_interest(
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.process_callback_check_interest(
            PersonalInterestsStage, callback, state)

    @staticmethod
    async def process_callback_go_page(
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.process_callback_go_page(
            PersonalInterestsStage, callback, state)

    @staticmethod
    async def process_callback_submit(
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.process_callback_submit(
            PersonalInterestsStage, callback, state)

    @staticmethod
    def register(router: Router) -> None:
        logging.info("PersonalInterestsStage was registered")
        BaseStage.register_base(PersonalInterestsStage, router)
